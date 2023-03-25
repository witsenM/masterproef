# Automatisch fotos nemen

* https://bc-robotics.com/tutorials/setting-cron-job-raspberry-pi/
* https://pimylifeup.com/cron-jobs-and-crontab/
* https://www.circuitbasics.com/starting-programs-automatically-using-cron-on-a-raspberry-pi/

# Processen data

* Open `opdrachtprompt`
* `cd masterproef`
* Haal laatste wijzigingen en fotos binnen: `git pull`
* Herbereken NDVI: `python berekenNDVI.py`
  * Fotos staan in `ndvi` map
  * `data.csv` bevat gemiddelde/standaardafwijking per foto
    * Openen in Excel via Data -> Import TXT/CSV, Tab, geen data type selectie
