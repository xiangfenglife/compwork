from ute_cloud_manager_api.api import CloudManagerApi
from ute_cloud_reservation_api.exception import ApiMaxReservationCountExceededException, \
    ApiWrongReservationStatusFoundException
from time import gmtime, strftime, sleep
import re, urllib

class ReservationHack:
    cloudManagersList = []

    def get_http(self, url):
        f = urllib.urlopen(url)
        myfile = f.read()
        return myfile

    def get_latest_build_name(self, build_regex):
        dict_sw_regex = {'FL17A' : 'FL17A_ENB_.{18}', 'FL00_FSM3' : 'FL00_FSM3_9999_.{13}', 'FL00_FSM4' : 'FL00_FSM4_9999_.{13}'}
        ute_enb_base_build_url = 'http://files.ute.inside.nsn.com/builds/enb/base/'
        ute_enb_base_build_url_content = self.get_http(ute_enb_base_build_url)
        build_list = re.findall(dict_sw_regex[build_regex], ute_enb_base_build_url_content)
        for build in reversed(build_list):
            given_build_url_content = self.get_http('{0}/{1}'.format(ute_enb_base_build_url,build))
            does_sw_exist = re.search('{}_release_BTSSM_downloadable.zip'.format(dict_sw_regex[build_regex]), given_build_url_content)
            if does_sw_exist:
                print 'Last existing SW build in UTE files is {}'.format(build)
                return build


    def createCloudManagersList(self, reservation_data):
        for user in reservation_data:
            self._createCloudManager(reservation_data[user])

    def createReservationForAllUsers(self):
        for cloudManager in self.cloudManagersList:
            self._createReservation(cloudManager[0], build_tag=cloudManager[2], testline_type=cloudManager[1])

    def extendReservationForAllUsers(self):
        for cloudManager in self.cloudManagersList:
            self._extendReservation(cloudManager[0])

    def releaseReservationForAllUsers(self):
        for cloudManager in self.cloudManagersList:
            self._releaseReservation(cloudManager[0])

    def _createCloudManager(self, user_data):
        self.cloudManagersList.append([CloudManagerApi(user_data[0]), user_data[1], user_data[2]])

    def _createReservation(self, cloudManager, build_tag, testline_type):
        latest_build_name = self.get_latest_build_name(build_tag)
        try:
            resId = cloudManager.create_reservation(testline_type=testline_type,
                                                    duration=420, state='configured', enb_build=latest_build_name)
            print "Reservation " + str(resId) + " started for " + str(cloudManager.api_token)
        except ApiMaxReservationCountExceededException:
            print "Oops! Max reservation count exceeded. Can't create more reservation for " + str(
                cloudManager.api_token)

    def _extendReservation(self, cloudManager):
        posibleResId = self._getPosibleToExtendReservationId(cloudManager)
        if posibleResId:
            try:
                cloudManager.extend_reservation(reservation_id=posibleResId[0], duration=180)
            except Exception:
                print "Can't extend reservation for " + str(cloudManager.api_token)
        else:
            print "Can't find any extendable reservation for " + str(cloudManager.api_token)

    def _releaseReservation(self, cloudManager):
        posibleResId = self._getPosibleToReleaseReservationId(cloudManager)
        if posibleResId:
            cloudManager.release_reservation(reservation_id=posibleResId[0])
            print "Release testline with id: " + str(posibleResId[0]) + " for " + str(cloudManager.api_token)

    def _getPosibleToExtendReservationId(self, cloudManager):
        try:
            return cloudManager.list_my_reservations(status='Confirmed', limit=1)
        except Exception:
            return {}

    def _getPosibleToReleaseReservationId(self, cloudManager):
        try:
            return cloudManager.list_my_reservations(limit=1)
        except Exception:
            return {}


class ReservationHackManager:
    rh = ReservationHack()
    reserved = False

    def __init__(self, reservation_data):
        self.rh.createCloudManagersList(reservation_data)

    def start(self):
        self.reserved = False
        start_time = int('00')  # starts at 8 o'clock
        release_time = int('12') # release at 21 o'clock

        while True:
            tmp_time = int(strftime("%H", gmtime()))
            print tmp_time
            if start_time <= tmp_time < (release_time-1):
                if self.reserved:
                    self.rh.extendReservationForAllUsers()
                    sleep(600)
                else:
                    self.reserved = True
                    self.rh.createReservationForAllUsers()
                    continue
            elif tmp_time == release_time:
                self.reserved = False
                self.rh.releaseReservationForAllUsers()
                sleep(3600)
            else:
                sleep(600)


reservation_data = {
#    'name' : ['token', 'cloud_tl_type', 'sw_tag_like_FL00_FSM3_or_FL00_FSM4_or_FL17A']       !!! make sure that cloud_tl_type match the sw_tag !!!
    'xbu' : ['770e07c3c8a3bed859db8ba8d5d0ef828c14aa30', 'CLOUD_R4P', 'FL17A']
}

rhm = ReservationHackManager(reservation_data)
rhm.start()
