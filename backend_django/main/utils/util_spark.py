from pyspark.sql import SparkSession, Catalog
from pyspark.context import SparkContext


# sc = SparkSession.builder.remote("sc://"+host+":7077")
# master = 'spark://39.108.175.203:7077'
# sc = SparkContext(master,appName="test")
# conf = sc.getConf()
# ss = SparkSession.builder.config(conf=conf).getOrCreate()
# df = ss.readStream.format("kafka").option("kafka.bootstrap.servers", "39.108.175.203:9092").option("subscribe", "test").load()

# df.writeStream.format("console").start()

spark=None

def validate_sparksession():
    if not spark.active():
        raise ValueError("spark is not started, please start it first")

def start_spark():
    global spark
    spark = SparkSession.builder \
                .master("local") \
                .appName("etlctl local driver") \
                .enableHiveSupport() \
                .getOrCreate()

def start_spark_remote():
    global spark
    spark = SparkSession.builder \
                .master("spark://39.108.175.203:7077") \
                .appName("etlctl remote driver") \
                .enableHiveSupport() \
                .getOrCreate()

local_file = "file:///home/dist/clue_data.csv"

def stop_spark():
    spark.stop()

def read_hive():
    # 读取hive表
    df = spark.sql("select count(1) from dim.dim_xl_account")
    df.show()


def read_csv(local_file):
    # 读取本地文件
    df = spark.read \
        .format("csv") \
        .option("header",True) \
        .load(local_file)
    return df


def read_csv2(local_file):
    df = spark.read.csv(local_file, header=True)
    return df


def write_to_table(df, table_name):
    df.write.mode("overwrite").saveAsTable(table_name)


def list_database(pattern="*"):
    catalog = spark.catalog
    result = catalog.listDatabases(pattern)
    return result

def list_tables(db_name = None):
    catalog = spark.catalog
    result = catalog.listTables(dbName = db_name)
    return result

def sc_env(key=None):
    sc = spark.sparkContext.getConf()
    if key:
        return sc.get(key)
    return sc.getAll()

def example():
    spark.sparkContext.parallelize(range(100)).map(lambda x: (x, 1)).reduceByKey(lambda a, b: a + b).collect().print()

if __name__=='__main__':
    # start_spark()
    start_spark_remote()
    # spark.sql("show databases").show()
    # df = read_csv(local_file)
    # write_to_table(df, 'tabB')
    # db_list = list_database()
    # print("database list : %s \n"%db_list)
    # tb_list = list_tables(db_name="ads")
    # print("table list : %s \n"%tb_list)
    print(sc_env("spark.master"))
    # stop_spark()




