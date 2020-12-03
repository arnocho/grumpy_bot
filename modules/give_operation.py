from mathparse import mathparse


def process(input_query):
    try:
        # Getting the mathematical terms within the input statement
        correct_format = input_query.replace("by", "*")
        expression = mathparse.extract_expression(correct_format, language="ENG")
        response = '{} = {}'.format(
            correct_format,
            mathparse.parse(expression, language="ENG")
        )
        return True
    except mathparse.PostfixTokenEvaluationException:
        return False


def action(input_module):
    try:
        correct_format = input_module.replace("by", "*")
        # Getting the mathematical terms within the input statement
        expression = mathparse.extract_expression(correct_format, language="ENG")
        response = '{} = {}'.format(
            expression,
            mathparse.parse(expression, language="ENG")
        )
        return response
    except mathparse.PostfixTokenEvaluationException:
        return None
