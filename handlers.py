import calendar
import datetime
import json
import logging
import time
import uuid
from logging.config import fileConfig

from flask import Flask, request, g, current_app
import psycopg2

from timeseries import *

fileConfig('logging_config.ini')
LOGGER = logging.getLogger()


class HandlerCdr:

    def __init__(self, FILE_PATH):
        self.FILE_PATH = FILE_PATH
        

    # logic for progress_mediamsec ... from cdr_new.php
    def get_progress_mediamsec(self, content):
        try:
            if int(content['variables']['progress_mediamsec']) > 0:
                return content['variables']['progress_mediamsec']
            else:
                return content['variables']['progressmsec']
        except Exception as e:
            return e

    def get_key_time(self, timestamp, granularity):
        return timestamp - (timestamp % TIME_DEFS[granularity]['factor'])

    def save_pg_data(self, sqlstring, record_to_insert):
        curr = g.db.cursor()
        try:
            record_to_insert = [
                None if cell == 'NULL' else cell for cell in record_to_insert
            ]
            LOGGER.debug("-----------------------------")
            LOGGER.debug(record_to_insert)
            LOGGER.debug("-----------------------------")
            curr.execute(sqlstring, record_to_insert)
            #
            curr.close()
            return True
        except Exception as e:
            LOGGER.error("unable to insert into postgres", e)
            raise
            return False

    def handle_inbound(self, content):
        LOGGER.debug(content)

        try:
            record_to_insert = (
                content['variables']['uuid'], content['variables']['peer_ip'],
                content['variables']['caller_id_name'],
                content['variables']['caller_id_number'],
                content['variables']['lrn'],
                content['variables']['destination_number'],
                content['variables']['direction'],
                content['variables']['context'],
                content['variables']['start_stamp'],
                content['variables']['progress_stamp'],
                content['variables']['answer_stamp'],
                content['variables']['end_stamp'],
                content['variables']['duration'],
                self.get_progress_mediamsec(content),
                content['variables']['billsec'],
                content['variables']['hangup_cause'],
                content['variables']['ep_codec_string'],
                content['variables']['dtmf_type'],
                content['variables']['remote_media_ip'],
                content['variables']['remote_media_port'],
                content['variables']['proto_specific_hangup_cause'],
                content['variables']['originate_disposition'],
                content['variables']['sip_term_status'],
                content['variables']['sip_term_cause'],
                content['variables']['hangup_cause_q850'],
                content['variables']['digits_dialed'],
                content['variables']['sip_hangup_disposition'],
                content['variables']['rtp_audio_in_quality_percentage'],
                content['variables']['rtp_audio_in_mos'],
                content['variables']['rtp_audio_out_packet_count'],
                content['variables']['rtp_audio_in_packet_count'],
                content['variables']['cdrtag'])
        except Exception as e:
            LOGGER.error(e)
            return '{"ERROR": "JSON_ERROR"}'

        if self.save_pg_data(self.sql_inbound_final(), record_to_insert):
            return '{"SUCCESS": "DATA INSERTED"}'
        else:
            self.err_save_file(json.dumps(content))
            return '{"ERROR": "DATA NOT SAVED"}'

    def handle_outbound(self, content):
        LOGGER.debug(content)
        try:
            record_to_insert = (
                content['variables']['uuid'],
                content['variables']['originator'],
                content['variables']['sip_to_host'],
                content['variables']['start_stamp'],
                content['variables']['start_uepoch'],
                content['variables']['answer_stamp'],
                content['variables']['end_stamp'],
                content['variables']['duration'],
                self.get_progress_mediamsec(content),
                content['variables']['bill_sec'],
                content['variables']['hangup_cause_q850'],
                content['variables']['ep_codec_string'],
                content['variables']['dtmf_type'],
                content['variables']['remote_media_ip'],
                content['variables']['remote_media_port'],
                content['variables']['billsec'],
                content['variables']['originate_disposition'],
                content['variables']['sip_term_status'],
                content['variables']['hangup_cause_q850'],
                content['variables']['digits_dialed'],
                content['variables']['sip_hangup_disposition'],
                content['variables']['rtp_quality'],
                content['variables']['rtp_audio_in_mos'],
                content['variables']['carrier_rate'],
                content['variables']['carrier'],
                content['variables']['hangup_cause_q850'],
                content['variables']['rtp_audio_out_packet_count'],
                content['variables']['rtp_audio_in_packet_count'],
                content['variables']['sip_term_cause'])
        except Exception as e:
            # LOGGER.error("unable to map json request to fields", e)
            LOGGER.error(e)
            return '{"ERROR": "JSON_ERROR"}'

        if (self.save_pg_data(self.sql_outbound_final(), record_to_insert) == True) and (self.update_redis_db(content) == True):
            return '{"SUCCESS": "DATA INSERTED"}'
        else:
            self.err_save_file(json.dumps(content))
            return '{"ERROR": "DATA NOT SAVED"}'



    def update_redis_db(self, content):
        # Handle redis business
        try:
            time_now = calendar.timegm(time.gmtime())
            key_hour = 'CARRIERSTATS::' + content['variables'][
                'carrier'] + '::' + str(get_key_time(time_now, "5Min"))
            if (content['variables']['hangup_cause'] == 'UNALLOCATED_NUMBER'):
                key404 = '404::' + content['callflow']['0']['caller_profile'][
                    'originator']['originator_caller_profiles']['0'][
                        'destination_number']
                g.redis.set(key404, 1)
                g.redis.setTimeout(key404, 30000)

            sip_key = 'SIP::' + content['variables']['hangup_cause']
            if (g.redis.hexists(key_hour, 'calls')):
                g.redis.hincrby(key_hour, 'calls', 1)
                g.redis.hincrby(key_hour, sip_key, 1)
            else:
                g.redis.hincrby(key_hour, 'calls', 1)
                g.redis.hincrby(key_hour, sip_key, 1)
                #TODO - set timeout with python lib ... no direct match with php lib
        except:
            LOGGER.error("error in redis update key_hour", e)
            raise
            return False
        try:
            if (int(content['variables']['billsec']) > 0):
                g.redis.hincrby(key_hour, 'answered', 1)
            if (int(content['variables']['billsec']) <= 6):
                g.redis.hincrby(key_hour, 'billsec_6', 1)
            elif (int(content['variables']['billsec']) <= 12):
                g.redis.hincrby(key_hour, 'billsec_12', 1)
            elif (int(content['variables']['billsec']) <= 18):
                g.redis.hincrby(key_hour, 'billsec_18', 1)
            elif (int(content['variables']['billsec']) <= 30):
                g.redis.hincrby(key_hour, 'billsec_30', 1)
            else:
                g.redis.hincrby(key_hour, 'billsec_31plus', 1)
        except:
            LOGGER.error("error updating billsec in redis", e)
            raise
            return False
        return True

    def check_db_status(self):
        sql = "SELECT 'HELLO WORLD'"
        cur = g.db.cursor()
        cur.execute(sql)
        res = cur.fetchone()[0]
        LOGGER.info(res)
        return res

    def handle_inbound_orig(self, content):
        try:
            record_to_insert = (
                content['variables']['sip_local_network_addr'],
                content['variables']['caller_id_name'],
                content['variables']['sip_from_Suser_stripped'],
                content['variables']['destination_number'],
                content['variables']['context'],
                content['variables']['start_stamp'],
                content['variables']['answer_stamp'],
                content['variables']['end_stamp'],
                content['variables']['duration'],
                content['variables']['billsec'],
                content['variables']['hangup_cause'],
                content['variables']['uuid'],
                content['variables']['bleg_uuid'],
                content['variables']['read_codec'],
                content['variables']['write_codec'],
                content['variables']['sip_hangup_disposition'],
                content['variables']['ani'], content['variables']['direction'],
                content['variables']['peer_ip'])
        except:
            LOGGER.error("unable to map json request to fields")
            raise
        print(sql_inbound_final())

    # Write file to filesystem --- for future processing
    def err_save_file(self, json):
        LOGGER.info("error processing json - saving as file")
        FILEPATH = "/tmp/"
        new_path = FILEPATH + str(uuid.uuid1()) + ".json"
        new_file = open(new_path, 'w')
        new_file.write(json)
        new_file.close()

    # Get year month format for table in postgres as in YYYYMM
    def get_year_month(self):
        now = datetime.datetime.now()
        return str(now.year) + str(now.month)

    # Return final table version
    def sql_inbound_final(self):
        return self.sql_inbound.replace('YYYY_MM', self.get_year_month())

    # Return final table version
    def sql_outbound_final(self):
        return self.sql_outbound.replace('YYYY_MM', self.get_year_month())

    # TODO cdr.term_a_ is correct format - cdr on local postgres .. investigate/change
    sql_inbound = """INSERT INTO cdr2.term_a_YYYY_MM
                        (uuid,
                        peer_ip,
                        caller_id_number,
                        ani,
                        lrn,
                        destination_number,
                        direction,
                        context,
                        start_stamp,
                        progress_stamp,
                        answer_stamp,
                        end_stamp,
                        duration,
                        progressmsec,
                        billsec,
                        hangup_cause,
                        ep_codec_string,
                        dtmf_type,
                        remote_media_ip,
                        remote_media_port,
                        proto_specific_hangup_cause,
                        originate_disposition,
                        sip_term_status,
                        sip_term_cause,
                        hangup_cause_q850,
                        digits_dialed,
                        sip_hangup_disposition,
                        rtp_quality,
                        rtp_mos,
                        rtp_audio_out_packet_count,
                        rtp_audio_in_packet_count,
                        cdrtag)
                VALUES(
                        %s, 
                        %s, 
                        %s, 
                        %s, 
                        %s, 
                        %s, 
                        %s, 
                        %s, 
                        %s, 
                        %s, 
                        %s, 
                        %s, 
                        %s, 
                        %s, 
                        %s, 
                        %s, 
                        %s, 
                        %s, 
                        %s, 
                        %s, 
                        %s, 
                        %s, 
                        %s, 
                        %s, 
                        %s, 
                        %s, 
                        %s, 
                        %s, 
                        %s, 
                        %s, 
                        %s, 
                        %s)"""

    # TODO cdr.term_a_ is correct format - cdr on local postgres .. investigate/change
    sql_outbound = """INSERT INTO cdr2.term_b_YYYY_MM
                (
                            uuid,
                            aleg_uuid,
                            peer_ip,
                            start_stamp,
                            progress_stamp,
                            answer_stamp,
                            end_stamp,
                            duration,
                            progressmsec,
                            billsec,
                            hangup_cause,
                            ep_codec_string,
                            dtmf_type,
                            remote_media_ip,
                            remote_media_port,
                            proto_specific_hangup_cause,
                            originate_disposition,
                            sip_term_status,
                            hangup_cause_q850,
                            digits_dialed,
                            sip_hangup_disposition,
                            rtp_quality,
                            rtp_mos,
                            rate,
                            carrier,
                            start_uepoch,
                            rtp_audio_out_packet_count,
                            rtp_audio_in_packet_count,
                            sip_term_cause
                )
                VALUES(
                %s, 
                %s, 
                %s, 
                %s, 
                %s, 
                %s, 
                %s, 
                %s, 
                %s, 
                %s, 
                %s, 
                %s, 
                %s, 
                %s, 
                %s, 
                %s, 
                %s, 
                %s, 
                %s, 
                %s, 
                %s, 
                %s, 
                %s, 
                %s, 
                %s, 
                %s, 
                %s, 
                %s, 
                %s)"""

    # TODO cdr.term_a_ is correct format - cdr on local postgres .. investigate/change
    sql_inbound_orig = """ INSERT INTO voip.cdr
                            ( 
                            local_ip_v4,
                            caller_id_name,
                            caller_id_number,
                            destination_number,
                            context,
                            start_stamp,
                            answer_stamp,
                            end_stamp,
                            duration,
                            billsec,
                            hangup_cause,
                            uuid,
                            bleg_uuid,
                            read_codec,
                            write_codec,
                            sip_hangup_disposition,
                            ani,
                            direction,
                            peer_ip)
                    VALUES     
                            (local_ip_v4,
                            caller_id_name,
                            caller_id_number,
                            destination_number,
                            context,
                            start_stamp,
                            answer_stamp,
                            end_stamp,
                            duration,
                            billsec,
                            hangup_cause,
                            uuid,
                            bleg_uuid,
                            read_codec,
                            write_codec,
                            sip_hangup_disposition,
                            ani,
                            direction,
                            peer_ip)"""
