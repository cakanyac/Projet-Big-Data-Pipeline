from pyspark.sql import SparkSession # type: ignore

# Créer la session Spark
spark = SparkSession.builder.appName("TestSpark").getOrCreate()

# Créer un DataFrame simple
data = [("Jean", 22), ("Fatou", 30), ("Akhi", 19)]
df = spark.createDataFrame(data, ["Nom", "Âge"])

# Affiche le contenu
df.show()
