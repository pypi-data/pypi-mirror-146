import time
from threading import Timer
import atexit
import pathlib
from datetime import datetime
import csv

from modular_client import ModularClient

try:
    from pkg_resources import get_distribution, DistributionNotFound
    import os
    _dist = get_distribution('lickport_array_interface_interface')
    # Normalize case for Windows systems
    dist_loc = os.path.normcase(_dist.location)
    here = os.path.normcase(__file__)
    if not here.startswith(os.path.join(dist_loc, 'lickport_array_interface_interface')):
        # not installed, but there is another version that *is*
        raise DistributionNotFound
except (ImportError,DistributionNotFound):
    __version__ = None
else:
    __version__ = _dist.version


DEBUG = False

class LickportArrayInterface():
    '''
    '''
    _DATA_PERIOD = 1.0
    _LICKED_STRING = 'L'
    _ACTIVATED_STRING = 'A'
    def __init__(self,*args,**kwargs):
        if 'debug' in kwargs:
            self.debug = kwargs['debug']
        else:
            kwargs.update({'debug': DEBUG})
            self.debug = DEBUG

        atexit.register(self._exit)

        self.controller = ModularClient(*args,**kwargs)
        self.controller.set_time(int(time.time()))
        self.controller.calibrate_lick_sensor()
        self._lickport_count = self._get_lickport_count()

        self._data_period = self._DATA_PERIOD
        self._base_path = pathlib.Path('~/lickport_array_data').expanduser()
        self._acquiring_data = False
        self._saving_data = False
        self._data_fieldnames = ['time',
                                 'millis']
        self._lickport_fieldnames = [f'lickport_{lickport}' for lickport in range(self._lickport_count)]
        self._data_fieldnames.extend(self._lickport_fieldnames)

    def _get_lickport_count(self):
        lickport_count = 0
        method_dict = self.controller.activate_lickport('??')
        method_parameters = method_dict['parameters']
        for method_parameter in method_parameters:
            if method_parameter['name'] == 'lickport':
                lickport_count = method_parameter['max'] + 1
        return lickport_count

    def start_acquiring_data(self,data_period=None):
        if data_period:
            self._data_period = data_period
        else:
            self._data_period = self._DATA_PERIOD
        self.controller.get_and_clear_lick_data()
        self._start_data_timer()
        self._acquiring_data = True

    def stop_acquiring_data(self):
        self._data_timer.cancel()
        self._acquiring_data = False

    def start_saving_data(self):
        data_directory_path = self._base_path / self._get_date_str()
        data_directory_path.mkdir(parents=True,exist_ok=True)
        data_filename = self._get_time_str() + '.csv'
        data_file_path = data_directory_path / data_filename
        self._data_file = open(data_file_path,'w')
        self._data_writer = csv.DictWriter(self._data_file,fieldnames=self._data_fieldnames)
        self._data_writer.writeheader()
        print('Created: {0}'.format(data_file_path))
        self._saving_data = True
        if not self._acquiring_data:
            self.start_acquiring_data()

    def stop_saving_data(self):
        self._saving_data = False
        self._data_file.close()

    def _save_datum(self,datum):
        if self._saving_data:
            lickports_licked = datum.pop('lickports_licked')
            licked_strings = [self._LICKED_STRING if lickport in lickports_licked else ''
                              for lickport in range(self._lickport_count)]
            lickports_activated = datum.pop('lickports_activated')
            activated_strings = [self._ACTIVATED_STRING if lickport in lickports_activated else ''
                                 for lickport in range(self._lickport_count)]
            lickport_strings = [''.join([i for i in x])
                                for x in zip(licked_strings,activated_strings)]
            lickport_datum = dict(zip(self._lickport_fieldnames,lickport_strings))
            datum = {**datum, **lickport_datum}
            self._data_writer.writerow(datum)

    def _handle_data(self):
        data = self.controller.get_and_clear_lick_data()
        for datum in data:
            print(datum)
            self._save_datum(datum)
        self._start_data_timer()

    def _start_data_timer(self):
        self._data_timer = Timer(self._data_period,self._handle_data)
        self._data_timer.start()

    def _exit(self):
        try:
            self.stop_saving_data()
            self.stop_acquiring_data()
        except AttributeError:
            pass

    def _get_datetime(self,timestamp=None):
        dt = None
        if timestamp is None:
            dt = datetime.fromtimestamp(time.time())
        else:
            dt = datetime.fromtimestamp(timestamp)
        return dt

    def _get_date_str(self,timestamp=None):
        dt = self._get_datetime(timestamp)
        date_str = dt.strftime('%Y-%m-%d')
        return date_str

    def _get_time_str(self,timestamp=None):
        dt = self._get_datetime(timestamp)
        time_str = dt.strftime('%H-%M-%S')
        return time_str



def main(args=None):
    lai = LickportArrayInterface()
    lai.start_saving_data()

# -----------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
