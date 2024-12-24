from enum import Enum

class DBState(Enum):
	deleted = "deleted"
	draft = "draft"

class UserRole(Enum):
	Supervisor = "Supervisor",
	Admin = "Admin",
	Carer = "Carer",
	Patient = "Patient"

class Gender(Enum):
	female = "female",
	male = "male",
	doctor = "doctor",
	professor = "professor"

class UserJob(Enum):
	podologue = "podologue",
	specialiste = "specialiste",
	centreReference = "centreReference",
	medecinTraitant = "medecinTraitant",
	infirmiere = "infirmiere",
	diabetologue = "diabetologue",

	developpeur = "developpeur",
	technicien = "technicien",
	adminsolsius = "adminsolsius",
	superadmin = "superadmin",
	logistique = "logistique",
	comptabilite = "comptabilite"

class AlertNotification(Enum):
	NO_INSOLES_ASSOCIATED = "NO_INSOLES_ASSOCIATED"
	SPEC_ERROR = "SPEC_ERROR"
	INCOHERENT_SENSORS = "INCOHERENT_SENSORS"
	TEMPERATURE_DATA_MISSING = "TEMPERATURE_DATA_MISSING"
	DATA_SYNCHRONISATION = "DATA_SYNCHRONISATION"
	END_OF_LIFE_BATTERY = "END_OF_LIFE_BATTERY"
	NOT_WEARING_INSOLES = "NOT_WEARING_INSOLES"
	TEMPERATURE_THRESHOLD_OVERPASS = "TEMPERATURE_THRESHOLD_OVERPASS"

class AlertActionType(Enum):
	none = "none"
	call = "call"
	callagain = "callagain"
	notify = "notify"
	validate = "validate"

class AlertStatus(Enum):
	created = "created"
	falsePositive = "falsePositive"
	verified = "verified"
	canceled = "canceled"
	terminated = "terminated"

class AlertType(Enum):
	temperature = "temperature"
	observance = "observance"
	technical = "technical"

class AlertTypeSub(Enum):
	spec = "sensorsSpec"
	incoherence = "sensorsIncoherence"
	loose = "sensorsLoose"
	weird = "sensorsWeird"