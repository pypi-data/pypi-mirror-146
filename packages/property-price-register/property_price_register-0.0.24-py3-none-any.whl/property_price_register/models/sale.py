import os
import re
import datetime
import glob
import tarfile
import statistics
import hashlib
import urllib.parse
from difflib import SequenceMatcher

import requests
from cached_property import cached_property
import pandas as pd

from eircode.address import Address
from property_price_register.utils import isnan


class Sales():

    def __init__(self, *args, **kwargs):
        self._data = kwargs.get('data', [])

    def contains(self, sale):
        return sale.content_hash in self.content_hashes

    def __getitem__(self, i):
        return self._data[i]

    def __iter__(self):
        return (i for i in self._data)

    def __len__(self):
        return len(self._data)

    def append(self, data):
        self._data.append(data)

    def extend(self, data):
        self._data.extend(data)

    def serialize(self):
        return [
            d.serialize() for d in self
        ]

    @cached_property
    def content_hashes(self):
        return set([d.content_hash for d in self._data])

    @staticmethod
    def from_file(filepath):
        data = None

        ext = os.path.splitext(filepath)[-1]
        if ext in {'.tgz', '.gz'}:
            tar = tarfile.open(filepath, 'r:gz')
            tar.extractall(path=os.path.dirname(filepath))
            tar.close()

            data = []
            for sub_file in glob.iglob(
                os.path.dirname(filepath) + '/**',
                recursive=True
            ):
                ext = os.path.splitext(sub_file)[-1]
                if ext == '.csv':
                    csv_data = pd.read_csv(
                        sub_file.replace('.csv.tgz', '.csv'),
                        encoding='ISO-8859-1'
                    ).to_dict(orient='records')
                    data.extend(csv_data)
        elif ext in {'.csv'}:
            data = pd.read_csv(
                filepath,
                encoding='ISO-8859-1'
            ).to_dict(orient='records')
        else:
            raise Exception()

        sales = Sales()
        for sales_dict in data:
            obj = Sale.parse(
                sales_dict
            )
            sales.append(obj)

        return sales

    @staticmethod
    def from_dir(dirpath):
        sales = Sales()
        search_dir = f'{dirpath}/**'
        for filename in glob.iglob(search_dir, recursive=True):
            if os.path.splitext(filename)[-1] not in {'.tgz', '.gz'}:
                continue
            sales.extend(
                Sales.from_file(
                    filename
                )
            )

        return sales

    def load():
        import property_price_register
        return Sales.from_dir(
            os.path.join(property_price_register.__path__[0], 'resources')
        )

    def save(self, filepath):
        df = pd.DataFrame(self.serialize())
        df = df.drop_duplicates(subset=['date', 'address', 'price', 'county'])
        df.to_csv(filepath)

    @property
    def average_price(self):
        return statistics.mean([s.price for s in self])


class Sale():

    def __init__(self, *args, **kwargs):

        if 'date' in kwargs:
            self.date = kwargs['date']
            self.address = kwargs['address']
            self.postal_code = kwargs['postal_code']
            self.county = kwargs['county']
            self.price = float(kwargs['price'])
            self.not_full_market_price = kwargs['not_full_market_price']
            self.vat_exclusive = kwargs['vat_exclusive']
            self.description_of_property = kwargs['description_of_property']
            self.description_of_property_size = kwargs['description_of_property_size']

            self._lat = kwargs['lat'] if not isnan(kwargs['lat']) else None
            self._lon = kwargs['lon'] if not isnan(kwargs['lon']) else None
            self._mapbox_address = kwargs['mapbox_address'] if not isnan(kwargs['mapbox_address']) else None
            self._mapbox_match_score = kwargs['mapbox_match_score'] if not isnan(kwargs['mapbox_match_score']) else None

            self._eircode_display_name = kwargs['eircode_display_name'] if 'eircode_display_name' in kwargs and not isnan(kwargs['eircode_display_name']) else None
            self._eircode_unique_id = kwargs['eircode_unique_id'] if 'eircode_unique_id' in kwargs and not isnan(kwargs['eircode_unique_id']) else None
            self._eircode_routing_key = kwargs['eircode_routing_key'] if 'eircode_routing_key' in kwargs and not isnan(kwargs['eircode_routing_key']) else None
            self._eircode_address_source = kwargs['eircode_address_source'] if 'eircode_address_source' in kwargs and not isnan(kwargs['eircode_address_source']) else None

        else:
            self.date = kwargs['Date of Sale (dd/mm/yyyy)']
            self.address = kwargs['Address']
            self.postal_code = kwargs['Postal Code'].replace('Baile Átha Cliath', 'Dublin').replace('Baile ?tha Cliath', 'Dublin') if not str(kwargs['Postal Code']) == 'nan' else None
            self.county = kwargs['County']
            self.price = float(kwargs['Price (\x80)'].replace('\x80', '').replace(',', ''))
            self.not_full_market_price = kwargs['Not Full Market Price']
            self.vat_exclusive = kwargs['VAT Exclusive']
            self.description_of_property = kwargs['Description of Property']
            self.description_of_property_size = kwargs['Property Size Description']

            self._lat = None
            self._lon = None
            self._mapbox_address = None
            self._mapbox_match_score = None

            self._eircode_display_name = None
            self._eircode_unique_id = None
            self._eircode_routing_key = None
            self._eircode_address_source = None

        if self.description_of_property not in [
            'Second-Hand Dwelling house /Apartment',
            'New Dwelling house /Apartment',
            'New Dwelling house /'
        ]:
            self.description_of_property = None

    @staticmethod
    def parse(data):
        if isinstance(data, Sale):
            return data

        return Sale(
            **data
        )

    def serialize(self):
        return {
            'date': self.date,
            'address': self.address,
            'postal_code': self.postal_code,
            'county': self.county,
            'price': self.price,
            'not_full_market_price': self.not_full_market_price,
            'vat_exclusive': self.vat_exclusive,
            'description_of_property': self.description_of_property,
            'description_of_property_size': self.description_of_property_size,
            'lat': self.lat,
            'lon': self.lon,
            'mapbox_address': self.mapbox_address,
            'mapbox_match_score': self.mapbox_match_score,
            'eircode_routing_key': self.eircode_routing_key,
            'eircode_unique_id': self.eircode_unique_id,
            'eircode_display_name': self.eircode_display_name,
            'eircode_address_source': self.eircode_address_source
        }

    @property
    def eircode_address_source(self):
        if self._eircode_address_source is None:
            return self._eircode_address_source

        if self._eircode_address_source is not None:
            return self._eircode_address_source

        if self.eircode_address[0] is None:
            return None

        return self.eircode_address[1]

    @property
    def eircode_routing_key(self):
        if self._eircode_routing_key is None:
            return self._eircode_routing_key

        if self._eircode_routing_key is not None:
            return self._eircode_routing_key

        if self.eircode_address[0] is None:
            return None

        if self.eircode_address[0].eircode.routing_key is not None:
            return self.eircode_address[0].eircode.routing_key

        return self.eircode_address[0].eircode.routing_key

    @property
    def eircode_unique_id(self):
        if self._eircode_unique_id is None:
            return self._eircode_unique_id

        if self._eircode_unique_id is not None:
            return self._eircode_unique_id

        if self.eircode_address[0] is None:
            return None

        if self.eircode_address[0].eircode.unique_identifier is not None:
            return self.eircode_address[0].eircode.unique_identifier

        return self.eircode_address[0].eircode.unique_identifier

    @property
    def eircode_display_name(self):
        if self._eircode_display_name is None:
            return self._eircode_display_name

        if self._eircode_display_name is not None:
            return self._eircode_display_name

        if self.eircode_address[0] is None:
            return None

        if self.eircode_address[0].display_name is not None:
            return self.eircode_address[0].display_name

        return self.eircode_address[0].display_name

    @cached_property
    def eircode_address(self):
        if self.mapbox_match_score is None:
            return (None, None)

        # TODO: choose best between self.address and self.mapbox_address (mapbox) and daft (in future). Maybe try all
        address = Address(self.address, throw_ex=False, proxy=True)
        if address.eircode.eircode is not None:
            return (address, 'ppr')

        # TODO: daft

        # FIXME: once daft is in then we can backup to mapbox
        if self.is_good_mapbox_address:
            mapbox_address = Address(self.mapbox_address, throw_ex=False, proxy=True)
            if mapbox_address.eircode.eircode is not None:
                return (mapbox_address, 'mapbox')

        return (
            Address(None, eircode=None, skip_set=True),
            None
        )

    @property
    def timestamp(self):
        return datetime.datetime.strptime(
            self.date,
            '%d/%m/%Y'
        )

    @property
    def year(self):
        return self.timestamp.year

    @cached_property
    def geo(self):
        if not os.environ.get('MAPBOX_TOKEN', None):
            return {
                'mapbox_address': None,
                'lat': None,
                'lon': None,
                'mapbox_match_score': None
            }

        location = urllib.parse.quote(self.address + ', ' + self.county)

        if len(location) > 100:
            return {
                'mapbox_address': None,
                'lat': None,
                'lon': None,
                'mapbox_match_score': None
            }

        try:
            data = requests.get('https://api.mapbox.com/geocoding/v5/mapbox.places/' + location + '.json?access_token=' + os.environ.get('MAPBOX_TOKEN', None) + '&country=ie').json()
            return {
                'mapbox_address': data['features'][0]['place_name'],
                'lat': data['features'][0]['center'][1],
                'lon': data['features'][0]['center'][0],
                'mapbox_match_score': data['features'][0]['relevance']
            }
        except:
            return {
                'mapbox_address': None,
                'lat': None,
                'lon': None,
                'mapbox_match_score': None
            }

    @property
    def lat(self):
        if self._lat is None:
            return self._lat

        if self._lat is not None:
            return float(self._lat)

        if self.geo['lat'] is not None:
            return float(self.geo['lat'])

        return self.geo['lat']

    @property
    def lon(self):
        if self._lon is None:
            return self._lon

        if self._lon is not None:
            return float(self._lon)

        if self.geo['lon'] is not None:
            return float(self.geo['lon'])

        return self.geo['lon']

    @property
    def mapbox_address(self):
        if self._mapbox_address is None:
            return self._mapbox_address

        if self._mapbox_address is not None:
            return self._mapbox_address

        if self.geo['mapbox_address'] is not None:
            return self.geo['mapbox_address']

        return self.geo['mapbox_address']

    @property
    def mapbox_match_score(self):
        if self._mapbox_match_score is None:
            return self._mapbox_match_score

        if self._mapbox_match_score is not None:
            return self._mapbox_match_score

        if self.geo['mapbox_match_score'] is not None:
            return self.geo['mapbox_match_score']

        return self.geo['mapbox_match_score']

    @property
    def content_hash(self):
        return hashlib.md5(
            f'{self.date}___{self.address}'.encode()
        ).hexdigest()

    @property
    def is_good_daft_address(self):
        raise NotImplementedError()

    @property
    def is_good_mapbox_address(self):
        try:
            if self.mapbox_match_score is None:
                return False
            if float(self.mapbox_match_score) < 0.6:
                return False
        except ValueError:
            return False

        # If there is a county in both, then make sure they match
        if self.county.lower() not in self.mapbox_address.lower():
            return False

        # TODO: Make sure if park / ave used in address that it isn't
        # contradicted in the mapbox address

        address_lower = self.address.lower()
        mapbox_lower = self.mapbox_address.lower()

        # See if number/number + letter are found in addresses
        if self.address[0].isdigit():
            starting_num_letter = re.findall(r'^\d+[a-zA-Z]*', self.address)[0].lower()
            if not mapbox_lower.startswith(starting_num_letter):
                return False

        if any([
            address_lower.startswith('apartment'),
            address_lower.startswith('flat'),
            address_lower.startswith('num'),
            address_lower.startswith('apt'),
            address_lower.startswith('no') and not address_lower.startswith('north'),
        ]):
            # FIXME: can also be NO5 or whatever
            # NOTE: if nos / nums / apartments then a range, can use
            # that somewhere

            cleaned = self.address
            if address_lower.startswith('number'):
                cleaned = address_lower.replace('number', '').strip()
            elif address_lower.startswith('apartment'):
                cleaned = address_lower.replace('apartment', '').strip()
            elif address_lower.startswith('flat'):
                cleaned = address_lower.replace('flat', '').strip()
            elif address_lower.startswith('apt'):
                cleaned = address_lower.replace('apt', '').strip()
            elif address_lower.startswith('num'):
                cleaned = address_lower.replace('num', '').strip()
            elif address_lower.startswith('no.'):
                cleaned = address_lower.replace('no.', '').strip()
            elif address_lower.startswith('no:'):
                cleaned = address_lower.replace('no:', '').strip()
            elif address_lower.startswith('no'):
                cleaned = address_lower.replace('no', '').strip()

            try:
                starting_num_letter = re.findall(r'^\d+[a-zA-Z]*', cleaned)[0].lower()
            except:
                # Doesn't start with nums, deal with this later
                return False

            if not mapbox_lower.startswith(starting_num_letter):
                return False

        # General string match check
        mapbox_match_score = SequenceMatcher(
            None,
            mapbox_lower,
            address_lower
        ).ratio()
        return mapbox_match_score >= 0.75
