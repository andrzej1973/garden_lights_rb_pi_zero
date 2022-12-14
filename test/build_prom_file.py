import os
import sys
import logging

LOG_ALL = True

#create two log file handlers, one for actual log file and another for stdout
stdout_handler = logging.StreamHandler(sys.stdout)

hndls = [stdout_handler]

if LOG_ALL == True:
    logging.basicConfig(level = logging.DEBUG,format = '%(asctime)s:%(threadName)s:%(filename)s:%(lineno)s:%(levelname)s:%(message)s', handlers=hndls)
else:
    logging.basicConfig(level = logging.INFO,format = '%(asctime)s:%(threadName)s:%(filename)s:%(lineno)s:%(levelname)s:%(message)s', handlers=hndls)

logging.debug('Loaded logging parameters:')
logging.debug('      Log All Information Incl. DEBUG logs: %s', LOG_ALL)


#build .prom file path - to be stored in same location as source file
idx=os.path.split(os.path.basename(__file__))[1].find('.')
file_name_wo_extension=os.path.split(os.path.basename(__file__))[1][:idx]
prom_file_path = os.path.dirname(os.path.realpath(__file__)) + "/" + file_name_wo_extension + ".prom"

#prom_file_path is dynamically linked to:/var/lib/prometheus/node-exporter/gardenpi.prom
#node exporter's text file collector
logging.info('Prometheus node exporters textfile collector path: %s', prom_file_path)

def PromMetrixSet(prom_file_p, loc_country, loc_city, loc_lat, loc_lon, lights_state): 
#It is assumed that PromMetrixSetLocation is always called prior to
#PromMetrixUpdate function
    
    locstr = "gardenpi_location{country=\"%s\",city=\"%s\",latitude=\"%s\",longitude=\"%s\"} 0\n" % (loc_country, loc_city, loc_lat, loc_lon)
    
    if os.path.exists(prom_file_p):
        #gardenpi_location{country="Poland",city="Otwock",latitude="52",longitude="21"} 0
        #gardenpi_lights_state ligths_state
        logging.debug('Prometheus node exporters textfile already exist - modifying it with:')
        logging.debug('   gardenpi_lights_state %s', lights_state)
        logging.debug('   %s', locstr)

        prom_file = open(prom_file_p,'r')
        filedata = prom_file.readlines()
        prom_file.close()
    
        prom_file = open(prom_file_p,'w')

        filedata[6] = locstr

        if lights_state == 0:
            #replace value 0 with 1
            filedata[2] = "gardenpi_lights_state 1\n"
        else:
            #replace value 1 with 0
            filedata[2] = "gardenpi_lights_state 0\n"
            
        prom_file.writelines(filedata)
        prom_file.close()
    
    else:
        logging.debug('Prometheus node exporters textfile does not exist - creating it with:')
        logging.debug('   gardenpi_lights_state %s', lights_state)
        logging.debug('   %s', locstr)

        prom_file = open(prom_file_p,'w')
        prom_file.write('# HELP gardenpi_lights_state Lights on/off indicator.\n')
        prom_file.write('# TYPE gardenpi_lights_state gauge\n')

        if lights_state  == 0:
            prom_file.write('gardenpi_lights_state 0\n')
        else:
            prom_file.write('gardenpi_lights_state 1\n')
            
        prom_file.write('\n')
        
        prom_file.write('# HELP gardenpi_location Information about geographical location of gardenpi controller\n')
        prom_file.write('# TYPE gardenpi_location gauge\n')
        prom_file.write(locstr)
        
        prom_file.close()


def PromMetrixUpdateLightsState(prom_file_p, value): 
#It is assumed that PromMetrixSetLocation is always called prior to this function!
#i.e. prom_file must already exist before this function is called 
    if os.path.exists(prom_file_p):
        
        logging.debug('Prometheus node exporters textfile already exist - modifying it with:')
        logging.debug('   gardenpi_lights_state %s', value)

        prom_file = open(prom_file_p,'r')
        filedata = prom_file.read()
        
        prom_file.close()
    
        prom_file = open(prom_file_p,'w')

        if value == 0:
            filedata = filedata.replace('gardenpi_lights_state 1','gardenpi_lights_state 0')
        else:
            filedata = filedata.replace('gardenpi_lights_state 0','gardenpi_lights_state 1')
            
        prom_file.write(filedata)
        prom_file.close()
    
    else:
        logging.debug('Prometheus node exporters textfile does not exist - creating it with:')
        logging.debug('   gardenpi_lights_state %s', value)

        prom_file = open(prom_file_p,'w')
        prom_file.write('# HELP gardenpi_lights_state Lights on/off indicator.\n')
        prom_file.write('# TYPE gardenpi_lights_state gauge\n')

        if value == 0:
            prom_file.write('gardenpi_lights_state 0\n')
        else:
            prom_file.write('gardenpi_lights_state 1\n')
            
        prom_file.close()
        
PromMetrixSet(prom_file_path, "Poland", "Otwock", "52", "21", 0)
#PromMetrixUpdateLightsState(prom_file_path, 1)
