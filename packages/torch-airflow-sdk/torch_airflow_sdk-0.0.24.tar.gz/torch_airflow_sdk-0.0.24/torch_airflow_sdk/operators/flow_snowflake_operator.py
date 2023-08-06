import base64
import logging

from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator

from torch_airflow_sdk.errors import FlowSnowflakeOperatorException

LOGGER = logging.getLogger("airflow.task")


class FlowSnowflakeOperator(SnowflakeOperator):
    def __init__(self, *, task_id, pipeline_uid=None, **kwargs) -> None:
        super(FlowSnowflakeOperator, self).__init__(task_id=task_id, **kwargs)
        self.pipeline_uid = pipeline_uid
        self.task_id = task_id
        if kwargs.get("sql"):
            self.sql = kwargs.get("sql")
            kwargs.pop('sql', None)
        if kwargs.get("snowflake_conn_id"):
            self.snowflake_connection_id = kwargs.get("snowflake_conn_id")
            kwargs.pop('snowflake_conn_id', None)
        elif kwargs.get("default_args"):
            default_arguments = kwargs.get("default_args")
            if default_arguments.get("snowflake_conn_id"):
                self.snowflake_connection_id = default_arguments.get("snowflake_conn_id")
            kwargs.pop('default_args', None)
        if kwargs.get("dag"):
            kwargs.pop('dag', None)
        self.additional_args = kwargs

    def execute(self, context):
        self.log.info("Execute body")
        self.log.info(context["dag"].default_args)
        encoded_message = ""
        if self.pipeline_uid:
            pipeline_comment = "pipelineUid=%s" % self.pipeline_uid
            ascii_message = pipeline_comment.encode("ascii")
            base64_byte_rep = base64.b64encode(ascii_message)
            encoded_message = base64_byte_rep.decode("ascii")
        # Statement logic
        if self.sql and not isinstance(self.sql, list) and not self.sql.strip().endswith(".sql"):
            self.log.info("Given SQL is a single statement")
            split_query = self.sql.split(" ", 1)
            # comments = json.dumps(self.json_map)
            self.sql = split_query[0] + ' /*' + encoded_message + '*/ ' + split_query[1]
        # Statement list logic
        elif self.sql and isinstance(self.sql, list):
            self.log.info("Given SQL is a statement list")
            modified_sql = []
            for statement in self.sql:
                if len(statement) != 0:
                    split_query = statement.split(" ", 1)
                    # comments = json.dumps(self.json_map)
                    modified_sql.append(split_query[0] + ' /*' + encoded_message + '*/ ' + split_query[1])
            self.sql = modified_sql
        # File logic
        elif self.sql and self.sql.strip().endswith(".sql"):
            self.log.info("Given SQL is a SQL File")
            file_name = self.sql.strip()
            fd = open(file_name, 'r')
            sql_statements = fd.read()
            fd.close()
            commands = sql_statements.split('\n')
            modified_sql_statements = ""
            comment_starts = False
            for cmd in commands:
                if not cmd.startswith('--'):
                    if cmd.startswith('/*'):
                        comment_starts = True
                        continue
                    elif cmd.endswith('*/'):
                        comment_starts = False
                        continue
                    elif not comment_starts:
                        modified_sql_statements = modified_sql_statements + cmd
            self.log.info(modified_sql_statements)
            sql_commands = modified_sql_statements.split(';')
            self.log.info(sql_commands)
            modified_sql = []
            for statement in sql_commands:
                self.log.info(statement)
                if len(statement) != 0:
                    split_query = statement.split(" ", 1)
                    # comments = json.dumps(self.json_map)
                    query = split_query[0] + ' /*' + encoded_message + '*/ ' + split_query[1]
                    self.log.info(query)
                    modified_sql.append(query)
            self.sql = modified_sql
        if self.sql and self.snowflake_connection_id:
            op = SnowflakeOperator(
                task_id=self.task_id,
                sql=self.sql,
                snowflake_conn_id=self.snowflake_connection_id,
                **self.additional_args
            )
            self.log.info(op.__dict__)
            try:
                op.execute(context)
            except Exception as e:
                self.log.error("Snowflake Operator execution failed for given parameters : %s and error message : %s " % (op.__dict__, str(e)))
                raise FlowSnowflakeOperatorException("Snowflake Operator execution failed")
        else:
            raise FlowSnowflakeOperatorException("No Valid parameters found for SnowflakeOperator")
