from sys import path
from os.path import dirname as dir
from shutil import rmtree

path.append(dir(path[0]))

from analizer.abstract import instruction as inst
from analizer import grammar
from analizer.reports import BnfGrammar


def execution(input):
    """
    docstring
    """
    querys = []
    messages = []
    result = grammar.parse(input)
    lexerErrors = grammar.returnLexicalErrors()
    syntaxErrors = grammar.returnSintacticErrors()
    if len(lexerErrors) + len(syntaxErrors) == 0:
        for v in result:
            if isinstance(v, inst.Select) or isinstance(v, inst.SelectOnlyParams):
                r = v.execute(None)
                if r:
                    list_ = r[0].values.tolist()
                    labels = r[0].columns.tolist()
                    print(list_)
                    querys.append([labels, list_])
                else:
                    querys.append(None)
            else:
                r = v.execute(None)
                messages.append(r)
    semanticErrors = grammar.returnSemanticErrors()
    PostgresErrors = grammar.returnPostgreSQLErrors()
    obj = {
        "messages": messages,
        "querys": querys,
        "lexical": lexerErrors,
        "syntax": syntaxErrors,
        "semantic": semanticErrors,
        "postgres": PostgresErrors,
    }
    return obj


def parser(input):
    """
    docstring
    """
    grammar.parse(input)
    lexerErrors = grammar.returnLexicalErrors()
    syntaxErrors = grammar.returnSintacticErrors()
    obj = {
        "lexical": lexerErrors,
        "syntax": syntaxErrors,
    }
    print(obj)
    return obj


s = """ 
USE test*;
select *
from tbrol WHERE idrol > 0;
"""
r = """ 
USE test[];
select *
from tbrol WHERE idrol > 0;
"""
# parser(s)
# execution(r)
# BnfGrammar.grammarReport()