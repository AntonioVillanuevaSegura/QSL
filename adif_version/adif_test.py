""" 
Antonio Villanueva Segura F4LEC 

Test adif 3.1.0

dépendances
pip install adif-io 

Référence ADIF
https://adif.org.uk/
https://www.adif.org.uk/310/ADIF_310.htm

adif validator
https://www.rickmurphy.net/adifvalidator.html

Modèle ADIF 3.1.0 récupéré à partir d'eqsl

Received eQSLs for F4LEC 
for QSOs between 04-Mar-2024 and 31-Dec-2034 and uploaded on or after 15-Oct-2013 00:00Z
Generated on Monday, October 14, 2024 at 09:59:26 AM UTC
<PROGRAMID:21>eQSL.cc DownloadInBox
<ADIF_Ver:5>3.1.0
<EOH>
<CALL:5>II2GM<QSO_DATE:8:D>20240322<TIME_ON:4>1724<BAND:3>40M<MODE:3>SSB<RST_SENT:2>59<RST_RCVD:0><QSL_SENT:1>Y<QSL_SENT_VIA:1>E<QSLMSG:24>TNX QSO - 73' II2GM Team<APP_EQSL_AG:1>Y<GRIDSQUARE:6>jn45sn<EQSL_QSL_RCVD:1>Y<EQSL_QSLRDATE:8>20240817 <EOR>

"""
import datetime

def creer_adif(contact):
	maintenant = datetime.datetime.now()

	date =  maintenant.strftime("%Y%m%d")
	#heure =  maintenant.strftime("%H%M%S")
	heure =  maintenant.strftime("%H%M")

	adif="<ADIF_Ver:5>3.1.0\n"
	adif += "<EOH>\n"
	adif += f"<CALL:{len(contact['CALL'])}>{contact['CALL']}"
	adif += f"<QSO_DATE:{ len( str (date))}>{date}"
	adif += f"<TIME_ON:{ len( str (heure))}>{heure}"
	adif += f"<BAND:{len(contact['BAND'])}>{contact['BAND']}"
	adif += f"<MODE:{len(contact['MODE'])}>{contact['MODE']}"
	adif += f"<RST_SENT:{len(contact['RST_SENT'])}>{contact['RST_SENT']}"
	adif += f"<RST_RCVD:{len(contact['RST_RCVD'])}>{contact['RST_RCVD']}"
	adif += "<EOR>\n"
    
	return adif


contact = {
	'CALL': 'F4LEC',
	'BAND': '40M',
	'MODE': 'SSB',
	'RST_SENT': '59',
	'RST_RCVD': '58',
	'QSL_SENT': 'Y',
	'QSL_SENT_VIA':'e',
	'QSLMSG':'TNX QSO - 73',
	'APP_EQSL_AG':'Y',
	'GRIDSQUARE':'jn45sn',
	'EQSL_QSL_RCVD':'Y',
	'EQSL_QSLRDATE':'20240817'
}

#Creer adif
adif_string = creer_adif(contact)

# Enregistrer dans un fichier
with open('mi_log.adi', 'a') as fichier:
    fichier.write(adif_string)

