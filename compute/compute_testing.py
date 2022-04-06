import traceback
from person import (
    format_person_name_first_last,
    compose_email_to_person_older_than_25
)
from author_list import (
    author_affiliation_text,
    create_affiliation_text_from_university_department
)
from academic_conference import (
    list_todays_conference_events
)
from utils import (
    Graph,
    read_json
)
from schema import (
    gen_data
)

class ComputeTester:
    def __init__(self, schema):
        self.schema = schema
        self.funcs = [
            format_person_name_first_last,
            compose_email_to_person_older_than_25,
            author_affiliation_text,
            create_affiliation_text_from_university_department,
            list_todays_conference_events
        ]
        entities = gen_data(schema)
        self.graph = Graph(entities=entities)
        self.audit_failures = []
        self.audit_functions = 0

    def audit_snippets(self, verbose=False):
        for func in self.funcs:
            self.audit_functions += 1
            self.audit_func_runs_against_schema(func)

        if verbose:
            if len(self.audit_failures) == 0:
                print(f"Functions are schema-compliant. Audited {self.audit_functions:,} function.")
            else:
                print("\n".join(self.audit_failures))

        return self.audit_failures

    def audit_func_runs_against_schema(self, func):
        """
        Check that a function runs against the provided schema

        Assumes that the first argument to the function is a type id and the second argument is a Graph
        """
        id_param = func.__code__.co_varnames[0]

        if self.check_id_param_is_recognised_type(func=func, id_param=id_param):

            args = {id_param: id_param, "graph": self.graph}

            try:
                func(**args)
            except Exception as e:
                self.audit_failures.append(f'Function: "{func.__name__}" does not comply with schema. Error message: "{str(e)}".')

    def check_id_param_is_recognised_type(self, func, id_param):
        graph_types = [x["@id"] for x in self.schema]
        try:
            assert id_param in graph_types
            return True
        except AssertionError:
            self.audit_failures.append(f'Function: "{func.__name__}" @id parameter @type: "{id_param}" is not present in schema.')
