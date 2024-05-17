CREATE (l:User { name: "lzy" })-[:FOLLOWS]->(q:User { name: "qyc" })
CREATE (q:User { name: "qyc" })-[:FOLLOWS]->(z:User { name: "zzy" })
CREATE (z:User { name: "zzy" })-[:FOLLOWS]->(y:User { name: "yyr" })
CREATE (y:User { name: "yyr" })-[:FOLLOWS]->(l:User { name: "lzy" })
RETURN l,q,z,y


CREATE CONSTRAINT ON (user:User) ASSERT user.name is UNIQUE