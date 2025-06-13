from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "rayanrayan"))

# Patients
def upsert_patient(patient):
    with driver.session() as session:
        session.run("""
            MERGE (p:Patient {id: $id})
            SET p.nom = $nom, p.prenom = $prenom, p.email = $email
        """, id=str(patient.id), nom=patient.nom, prenom=patient.prenom, email=patient.email)

def delete_patient(patient_id):
    with driver.session() as session:
        session.run("MATCH (p:Patient {id: $id}) DETACH DELETE p", id=str(patient_id))

# Médecins
def upsert_medecin(medecin):
    with driver.session() as session:
        session.run("""
            MERGE (m:Medecin {id: $id})
            SET m.nom = $nom, m.prenom = $prenom, m.email = $email, m.specialite = $specialite
        """, id=str(medecin.id), nom=medecin.nom, prenom=medecin.prenom, email=medecin.email, specialite=medecin.specialite)

def delete_medecin(medecin_id):
    with driver.session() as session:
        session.run("MATCH (m:Medecin {id: $id}) DETACH DELETE m", id=str(medecin_id))

# Consultation
def create_consultation_relation(consultation):
    with driver.session() as session:
        session.run("""
            MATCH (p:Patient {id: $patient_id}), (m:Medecin {id: $medecin_id})
            MERGE (p)-[:CONSULTE {date: $date}]->(m)
        """, patient_id=str(consultation.patient.id), medecin_id=str(consultation.medecin.id), date=str(consultation.date))

def delete_consultation_relation(consultation):
    with driver.session() as session:
        session.run("""
            MATCH (p:Patient {id: $patient_id})-[r:CONSULTE]->(m:Medecin {id: $medecin_id})
            WHERE r.date = $date
            DELETE r
        """, patient_id=str(consultation.patient.id), medecin_id=str(consultation.medecin.id), date=str(consultation.date))
