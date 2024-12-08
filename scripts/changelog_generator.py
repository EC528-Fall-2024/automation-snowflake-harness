import yaml
import logging
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.snowflake_manager import connect_to_snowflake

def get_database_objects():
    objects = {
        'tables': [],
        'views': [],
        'sequences': []
    }
    
    conn = connect_to_snowflake()
    try:
        with conn.cursor() as cursor:
            # Get tables
            cursor.execute("SHOW TABLES")
            objects['tables'] = [
                {'name': row[1], 'schema': row[3]} 
                for row in cursor.fetchall() 
                if row[1] not in ('DATABASECHANGELOG', 'DATABASECHANGELOGLOCK')
            ]

            # Get views
            cursor.execute("SHOW VIEWS")
            objects['views'] = [{'name': row[1], 'schema': row[3]} for row in cursor.fetchall()]

            # Get sequences
            cursor.execute("SHOW SEQUENCES")
            objects['sequences'] = [{'name': row[1], 'schema': row[3]} for row in cursor.fetchall()]

        logging.info("Successfully retrieved database objects.")
    except Exception as e:
        logging.error(f"Error retrieving database objects: {str(e)}")
        raise
    finally:
        conn.close()

    return objects

def generate_unique_id(prefix, obj):
    return f"{prefix}-{obj['schema']}-{obj['name']}"

def generate_changelog(objects):
    changelog = []
    changelog.append({
        'changeSet': {
            'id': 'create-template-warehouse',
            'author': 'dynamic-generator',
            'changes': [{
                'sql': {
                    'sql': """
                    CREATE WAREHOUSE IF NOT EXISTS template_warehouse
                    WAREHOUSE_SIZE = 'SMALL'
                    AUTO_SUSPEND = 300
                    AUTO_RESUME = TRUE
                    INITIALLY_SUSPENDED = TRUE
                    SCALING_POLICY = 'STANDARD';
                    """
                }
            }]
        }
    })
    changelog.append({
        'changeSet': {
            'id': 'create-test-table',
            'author': 'dynamic-generator',
            'changes': [{
                'createTable': {
                    'schemaName': 'PUBLIC',  # 目标schema
                    'tableName': 'test_table',  # 目标表名
                    'columns': [
                        {
                            'column': {
                                'name': 'id',
                                'type': 'INT',
                                'constraints': {
                                    'primaryKey': True,
                                    'nullable': False
                                }
                            }
                        },
                        {
                            'column': {
                                'name': 'name',
                                'type': 'VARCHAR(255)',
                                'constraints': {
                                    'nullable': True
                                }
                            }
                        }
                    ]
                }
            }],
            'rollback': [{
                'dropTable': {
                    'schemaName': 'PUBLIC',
                    'tableName': 'test_table'
                }
            }]
        }
    })
    for table in objects['tables']:
        changelog.append({
            'changeSet': {
                'id': generate_unique_id('create-table', table),
                'author': 'dynamic-generator',
                'changes': [{
                    'createTable': {
                        'schemaName': table['schema'],
                        'tableName': table['name'],
                        'columns': [
                            {'column': {'name': 'id', 'type': 'INT', 'autoIncrement': True, 'constraints': {'primaryKey': True, 'nullable': False}}}
                        ]
                    }
                }],
                'rollback': [{'dropTable': {'schemaName': table['schema'], 'tableName': table['name']}}] # Add rollback for table creation

            }
        })
    
    for view in objects['views']:
        changelog.append({
            'changeSet': {
                'id': generate_unique_id('create-view', view),
                'author': 'dynamic-generator',
                'changes': [{
                    'createView': {
                        'schemaName': view['schema'],
                        'viewName': view['name'],
                        'selectQuery': f'SELECT * FROM {view["schema"]}.{view["name"]}'
                    }
                }],
                'rollback': [{'dropView': {'schemaName': view['schema'], 'viewName': view['name']}}] # Add rollback for view creation

            }
        })
    
    for sequence in objects['sequences']:
        changelog.append({
            'changeSet': {
                'id': generate_unique_id('create-sequence', sequence),
                'author': 'dynamic-generator',
                'changes': [{
                    'createSequence': {
                        'schemaName': sequence['schema'],
                        'sequenceName': sequence['name'],
                        'startValue': 1,
                        'incrementBy': 1
                    }
                }],
                'rollback': [{'dropSequence': {'schemaName': sequence['schema'], 'sequenceName': sequence['name']}}] # Add rollback for sequence creation
            }
        })

    logging.info(f"Total changesets generated: {len(changelog)}")
    return changelog

def write_changelog_to_file(changelog, filename):
    try:
        with open(filename, 'w') as file:
            yaml.dump({'databaseChangeLog': changelog}, file, sort_keys=False)
        logging.info(f"Changelog written to {filename}")
    except Exception as e:
        logging.error(f"Error writing changelog to file: {str(e)}")
        raise

def create_dynamic_changelog(output_file):
    objects = get_database_objects()
    changelog = generate_changelog(objects)
    write_changelog_to_file(changelog, output_file)