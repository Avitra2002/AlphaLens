from neo4j import GraphDatabase
from config.settings import NEO4J_PASSWORD, NEO4J_URI, NEO4J_USERNAME


def save_to_neo4j(relationships):
    driver = GraphDatabase.driver(
        NEO4J_URI, 
        auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
    )

    with driver.session() as session:
        for rel in relationships:
            session.run(
                """
                MERGE (a:Company {name: $entity1})
                MERGE (b:Company {name: $entity2})
                MERGE (a)-[r:RELATIONSHIP {type: $relationship_type}]->(b)
                SET r.confidence = $confidence,
                    r.context = $context
                """,
                entity1=rel.entity1,
                entity2=rel.entity2,
                relationship_type=rel.relationship_type,
                confidence=rel.confidence,
                context=rel.context
            )

    driver.close()
