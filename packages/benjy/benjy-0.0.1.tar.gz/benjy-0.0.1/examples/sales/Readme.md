# Company Sales

In this demo we will walk through setting up and using Benjy with example data from a fake company. 
This company has sales from three different sources `a`, `b`, and `c`. Although the company uses a universal customer
id called `uuid` each source uses its' own, distinct, id. 

We are going to combine all three sources, normalize to the `uuid` customer id, and aggregate sales in 4 hour intervals - all
without _having_ to write SQL.

## Getting started

First, we will need to simulate some fake data for the project. You can do that by executing the `make_data.py` script 
from this directory. We will also need to install a copy of benjy to get started.

```bash
pip install benjy
python make_data.py
```

Inside the `/project` subdirectory you will see three folders:

1. `data` - this contains the raw data resources we will be writing ETL's for. In our case we have sales records coming from three different sources (a, b, and c) each with different customer identifiers. We also have crosswalks between customer ids to a universal identifier shared across data sources. 
2. `entities` - these represent relationships between our data. In this case we have an entity for each customer id. These entities have a couple of attributes including the source table, the column id of the source, and a relationship between the source id and the universal id.
3. `output` - Where we are going to place our ETL output.

Finally, we have a `schema.yml` file. These are declarative yaml files defining the expected output of a transformation.

## Using Benjy

In order to automatically perform an ETL, Benjy first compiles your entities into a graph of relationships between data sources. 
Let's give that a shot -

```bash
cd project
benjy compile .
```

These compiled results are stored in the `build` subdirectory of our folder. We are now ready to execute our own ETL. 

```bash
benjy submit schema.yaml
```

Voila! Checkout the `/output` folder to find your ETL'ed data.


## Exploring Further

The default `schema.yaml` looks like this

```yaml
target: 'output/result_table.csv'
driver: 'python'
sources:
  - 'sales_source_a_table'
  - 'sales_source_b_table'
  - 'sales_source_c_table'
name: 'aggregate_sales'
columns:
  - name: 'uuid'
    entity: 'uuid'
    origin: 'id'
    keyed: true
  - name: 'timestamp'
    origin: 'ts'
    type:
      datatype: 'timestamp'
      frequency: 4h
  - name: 'sales'
    origin: 'sales'
    type:
      datatype: 'integer'
```

Much of this will be self-explanatory; We have a few sources we wish to draw data from, a location we want to place our 
result, and a name for our result. The meat of the actual query definition falls under `columns`.

First, if you look at the `uuid` column in the output file you'll see customer id's that look like `01639fb9-7bd7-43c3-afe3-b9eeef5901b7` despite
the ID's in `a`, `b` and `c` being Integers. How'd it do that? 

Each of these ids are "entities" within Benjy - basically reusable components of your organizations' data. Let's take a look
at the `source_a_id` entity in `entities/sales_source_a_table.yaml`.


```yaml
entities:
  - name: source_a_id
    source: sales_source_a_table
    column: id
    relations:
      - name: uuid
        crosswalk:
          source: crosswalk_uuid_a_table
          from: id_a
          to: uuid
```

Again, this is mostly-self explanatory - the entity, has a `name` we can reference and re-use in each ETL workflow, a `source` 
corresponding to the table it can be queried from, and the specific `column` it belongs to in the source. However, it also
has a `relations` attribute. In this case the relation describes a crosswalk between it and the universal id `uuid`.


Thanks to these entities, Benjy knows how to query for `uuid` values when provided with simple `id` from any of our three
sales sources and can perform that process for us even if it requires many steps or transformations to achieve.

There's a lot more here - try it yourself - would you prefer sales were floats rather than integers? Change the datatype to `float`. How about 
aggregating sales daily? Switch the frequency to `d`. Maybe you don't want to perform any aggregation? Remove the frequency
argument on the timestamp column and the keyed argument on uuid!


### TODO
- [ ] currently requires python / pandas to generate data. Maybe migrate this to a separate repo and stick the data in vc.