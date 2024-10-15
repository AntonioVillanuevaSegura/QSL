""" 
Antonio Villanueva Segura F4LEC 

Classe pour gérer l'adif

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
import os

class Adif():
	""" Classe pour ecrire l'Adif dans un fichier externe  vous devez saisir les données du qso"""
	def __init__(self):	
		self.contact = {
			'CALL': None,
			'BAND': None,
			'MODE': None,
			'RST_SENT': None,
			'RST_RCVD': None,
			'QSL_SENT': None,
			'QSL_SENT_VIA': None,
			'QSLMSG': None,
			'APP_EQSL_AG': None,
			'GRIDSQUARE': None,
			'EQSL_QSL_RCVD': None,
			'EQSL_QSLRDATE': None
		}
		self.programid="F4LEC_soft"
		self.adif_version="3.1.0"
		self.adif=None #Text adif
		self.fichier='mi_log.adi' #Nom fichier externe
	
	def valeur_vide(self,valeur):
		""" valeur null"""
		return valeur is None	
	
	def set_contact (self,contact):
		""" Set self.contact local avec dict. contact externe dict."""
		for key,value in contact.items():
			self.contact[key]=value
			
	def creer_adif(self):
		"""Créer une chaîne adif  """
		# check l'existence du fichier adif 
		check = self.check()
		
		maintenant = datetime.datetime.now()

		date =  maintenant.strftime("%Y%m%d")
		#heure =  maintenant.strftime("%H%M%S")
		heure =  maintenant.strftime("%H%M")
		
		self.adif=""
		if (not self.valeur_vide(self.programid) and not (check)):
			self.adif =f"<PROGRAMID:{len(self.programid)}>{self.programid}\n"
			
		if (not self.valeur_vide(self.adif_version)  and not (check)):						
			self.adif +=f"<ADIF_Ver:{len(self.adif_version)}>{self.adif_version}\n"
		
		if ( not (check)):	
			self.adif += "<EOH>\n"
			
		if not(self.valeur_vide(self.contact['CALL'])):
			self.adif += f"<CALL:{len(self.contact['CALL'])}>{self.contact['CALL']}"
			
		if not(self.valeur_vide(date)):
			self.adif += f"<QSO_DATE:{ len( str (date))}>{date}"
			
		if not(self.valeur_vide(str (heure))):		
			self.adif += f"<TIME_ON:{ len( str (heure))}>{heure}"
			
		if not(self.valeur_vide(self.contact['BAND'])):		
			self.adif += f"<BAND:{len(self.contact['BAND'])}>{self.contact['BAND']}"
			
		if not(self.valeur_vide(self.contact['MODE'])):		
			self.adif += f"<MODE:{len(self.contact['MODE'])}>{self.contact['MODE']}"
			
		if not(self.valeur_vide(self.contact['RST_SENT'])):		
			self.adif += f"<RST_SENT:{len(self.contact['RST_SENT'])}>{self.contact['RST_SENT']}"
			
		if not(self.valeur_vide(self.contact['RST_RCVD'])):		
			self.adif += f"<RST_RCVD:{len(self.contact['RST_RCVD'])}>{self.contact['RST_RCVD']}"
			
		if not(self.valeur_vide(self.contact['QSL_SENT'])):		
			self.adif += f"<QSL_SENT:{len(self.contact['QSL_SENT'])}>{self.contact['QSL_SENT']}"	
			
		if not(self.valeur_vide(self.contact['QSL_SENT_VIA'])):		
			self.adif += f"<QSL_SENT_VIA:{len(self.contact['QSL_SENT_VIA'])}>{self.contact['QSL_SENT_VIA']}"
			
		if not(self.valeur_vide(self.contact['QSLMSG'])):		
			self.adif += f"<QSLMSG:{len(self.contact['QSLMSG'])}>{self.contact['QSLMSG']}"
				
		if not(self.valeur_vide(self.contact['APP_EQSL_AG'])):		
			self.adif += f"<APP_EQSL_AG:{len(self.contact['APP_EQSL_AG'])}>{self.contact['APP_EQSL_AG']}"
				
		if not(self.valeur_vide(self.contact['GRIDSQUARE'])):		
			self.adif += f"<GRIDSQUARE:{len(self.contact['GRIDSQUARE'])}>{self.contact['GRIDSQUARE']}"
				
		if not(self.valeur_vide(self.contact['EQSL_QSL_RCVD'])):		
			self.adif += f"<EQSL_QSL_RCVD:{len(self.contact['EQSL_QSL_RCVD'])}>{self.contact['EQSL_QSL_RCVD']}"
			
		if not(self.valeur_vide(self.contact['EQSL_QSLRDATE'])):		
			self.adif += f"<EQSL_QSLRDATE:{len(self.contact['EQSL_QSLRDATE'])}>{self.contact['EQSL_QSLRDATE']}"					
		self.adif += "<EOR>\n"
		
		self.write () #Ecrire Adif dans un fichier externe
		
		return self.adif

	def write(self):
		""" write adif file with adif data """
		with open(self.fichier, 'a') as fichier:
			fichier.write(self.adif)
			
	def exist_file(self):
		""" Check for the existence of a file use in check  """
		if os.path.exists(self.fichier):
			return True
		else:
			return False
								
	def check(self):	
		""" analyse l'existence du fichier et son contenu"""
		if not (self.exist_file ()):
			return False	
		
		# open fichier
		try:
			with open(self.fichier, 'r') as text:
				contenu = text.read()
		except IOError as e:
			return False
				
		# test words in fichier 
		# Check PROGRAMID ADIF_Ver EOH 
		tests=("PROGRAMID","ADIF_Ver","EOH")
		
		for test in tests:
			if test in contenu :
				return True
		
		return False		
			

""" Exemple de données de QSO de contact"""		
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


#Cree une instance classe Adif
contact_adif =Adif() 

#Set le contact QSO  dans l'instance de la classe Adif 
contact_adif.set_contact(contact)

#Cree  le string Adif et ecrire adif
contact_adif.creer_adif()


 

