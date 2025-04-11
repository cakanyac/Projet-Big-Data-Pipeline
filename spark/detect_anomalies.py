from pyspark.sql import SparkSession # type: ignore
from pyspark.ml.clustering import KMeans # type: ignore
from pyspark.ml.feature import VectorAssembler # type: ignore
from pyspark.sql.functions import col, udf # type: ignore
from pyspark.sql.types import DoubleType # type: ignore

# Créer une session Spark
spark = SparkSession.builder \
    .appName("AnomalyDetectionO3") \
    .getOrCreate()

# Lire le fichier JSON
df = spark.read.option("multiline", "true").json("from_kafka.json")

# Préparation : transformer la colonne "value" en vecteur
vec_assembler = VectorAssembler(inputCols=["value"], outputCol="features")
df_vector = vec_assembler.transform(df)

# Appliquer KMeans
kmeans = KMeans(k=2, seed=1, featuresCol="features", predictionCol="cluster")
model = kmeans.fit(df_vector)
centers = model.clusterCenters()

# Ajouter les clusters au DataFrame
df_clusters = model.transform(df_vector)

# Fonction pour calculer la distance au centre du cluster
def distance_to_center(value, cluster):
    return float(abs(value - centers[cluster][0]))

distance_udf = udf(distance_to_center, DoubleType())
df_distance = df_clusters.withColumn("distance", distance_udf(col("value"), col("cluster")))

# Seuil : moyenne des distances * 1.5
mean_distance = df_distance.selectExpr("avg(distance) as avg").first()["avg"]
threshold = mean_distance * 1.5

# Détection d'anomalies
df_result = df_distance.withColumn("anomaly", (col("distance") > threshold))

# Affichage des anomalies
anomalies = df_result.filter(col("anomaly") == True)
anomalies.select("datetime", "value", "anomaly").show(truncate=False)

# Sauvegarde
anomalies.select("datetime", "value", "anomaly").write.mode("overwrite").json("anomalies_detected.json")

spark.stop()
