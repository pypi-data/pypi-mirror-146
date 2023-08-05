# from base_logger import logging
# from Config import Config
# import utils as Utils

from bomancli import utils as Utils
from bomancli.base_logger import logging
from bomancli.Config import Config


import yaml
import json
import requests
import os


#### read the input from the yaml file -- MM ------------------------------------------------------------

def yamlValidation():

    logging.info('Finding boman.yaml file')

    try: 
        with open('boman.yaml', 'r') as file:
            Config.config_data = yaml.safe_load(file)    
        logging.info('Config yaml file found')    
    except:
        
        logging.error('No config yaml file found')
        exit(-1)

    logging.info('Prasing and Validating the config yaml file')
   


    try:
        Config.config_data['Auth']
        if Config.config_data['Auth'] != '':
            Config.app_token = Config.config_data['Auth']['project_token']
            Config.customer_token =Config.config_data['Auth']['customer_token']


    except KeyError:

        logging.error('Project and Customer token is mandatory to run the scan. Refer the documentation.')    


    try: 

        if  Config.config_data['SAST'] != '':
            Config.sast_lang = Config.config_data['SAST']['language'].split(",") ## comma sperated if mulitple
            
            Config.sast_present = True

            logging.info('SAST is properly configured with %s and ready to scan',Config.sast_lang)

            try:
                Config.sast_build_dir  = Config.config_data['SAST']['work_dir']
            except KeyError: 
                Config.sast_build_dir = os.getcwd()+'/'

        if 'java' in Config.sast_lang:

            try:
                Config.sast_target =  Config.config_data['SAST']['target']
            except KeyError: 
                logging.error('Java requires a target file to be mentioned in the boman.yaml file. refer the documentation')
                Config.sast_present = False       
    except KeyError:    
        Config.sast_present = False
        logging.warning('SAST was not properly defined in the config')
        logging.warning('Ignoring SAST, Please provide all mandatory inputs incase you like to run SAST scan.')
        

    
    ## DAST

    try: 
        Config.dast_target = Config.config_data['DAST']['URL']
        Config.dast_type = Config.config_data['DAST']['type']

        Config.dast_present = True

        try:        
            if Config.config_data['DAST']['cred'] == 'true':
                Config.dast_cred = True
                Config.dast_uname = Config.config_data['DAST']['username']
                Config.dast_password = Config.config_data['DAST']['password']
        except KeyError:
            Config.dast_cred_present = False 


        if Utils.testDastUrl(Config.dast_target):
            logging.info('DAST is properly configured and ready to scan')
        else:    
            logging.info('DAST target is not reachable, ignoring DAST scan')
            Config.dast_present = False
                
    except KeyError:    
        Config.dast_present = False
        logging.warning('DAST was not properly defined in the config.')
        logging.warning('Ignoring DAST, Please provide all mandatory inputs incase you like to run DAST scan.')
        



    ## SCA

    try: 
        if  Config.config_data['SCA'] != '':
            Config.sca_lang = Config.config_data['SCA']['language'].split(",") ## comma sperated if mulitple
            
            Config.sca_present =  True

            try:
                Config.sca_build_dir = Config.config_data['SCA']['work_dir']
            except KeyError: 
                Config.sca_build_dir = os.getcwd()+'/'

            logging.info('SCA is properly configured and ready to scan')    
    except KeyError:    
        Config.sca_present =  False
        logging.warning('SCA was not properly defined in the config')
        logging.warning('Ignoring SCA, Please provide all mandatory inputs incase you like to run SCA scan.')
        
##secret scann
    try:
        if Config.config_data['Secret_Scan'] == False:
            Config.secret_scan_present = False
        else:   
            try:
                Config.sast_build_dir  = Config.config_data['SAST']['work_dir']
            except KeyError: 
                Config.sast_build_dir = os.getcwd()+'/'
                 
            try:
                Config.secret_scan_present =  True if Utils.isGitDirectory(Config.sast_build_dir) else False

                if Config.secret_scan_present:
                    logging.info('Secret scanning is properly configured and ready to scan')
                else:
                    logging.warning('Secret scanning is properly configured, but working directory is not a git repository.') 
                    logging.warning('Ignoring Secret scanning.')                 
            except KeyError:
                Config.secret_scan_present = False
                logging.warning('Secret scanning is not properly configured, Working directory is not git.') 
    except KeyError:
        Config.secret_scan_present = False  
        logging.warning('Secret scanning is not properly configured. Cant read the Secret_Scan configuration.')   

        

    

## need to use lingudetect here, but the results are not trustable and misleading ------ MM -------------------
def findLang():
    print('[INFO]: Detecting Language')
