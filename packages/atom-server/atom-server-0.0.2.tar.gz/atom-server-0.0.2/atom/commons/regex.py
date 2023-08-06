import re


def matchURI(rule, uri):
    original_rule = rule
    if (uri == '' or uri == '/') and rule == '/':
        return True, {}, '/'
    if not rule.startswith('/'):
        rule = f"/{rule}"
    if not rule.endswith('/'):
        rule = f"{rule}/"
    if not uri.startswith('/'):
        uri = f"/{uri}"
    if not uri.endswith('/'):
        uri = f"{uri}/"
    regex = _ruleToRegex(rule)
    if regex:
        if re.fullmatch(regex, uri):
            return True, _uriToParams(rule, uri), original_rule
    return False, {}, None


def _ruleToRegex(rule):
    output = re.fullmatch(r"^\/(.+.*)\/$", rule)
    if output is not None:
        tokens = rule.split('/')
        tokens = tokens[1: len(tokens) - 1]
        pattern_tokens = []
        for token in tokens:
            if re.fullmatch(r"^\{([\w_]+):(\bint|str|bool|float\b)\}$", token):
                groups = re.findall(r"^\{([\w_]+):(\bint|str|bool|float\b)\}$", token)
                match = groups[0][1]
                if match == 'int':
                    pattern_tokens.append("([0-9]+)")
                elif match == 'str':
                    pattern_tokens.append("([\w_\-@]+[\w\s_\-@.+\\=]*)")
                elif match == 'bool':
                    pattern_tokens.append("(true|false)")
                elif match == 'float':
                    pattern_tokens.append("(\d+\.\d+)")
            else:
                pattern_tokens.append(token)
        return "/" + "/".join(pattern_tokens) + "/"
    return False


def _uriToParams(rule, uri):
    param = {}
    rule_to_tokens = rule.split('/')
    rule_to_tokens = rule_to_tokens[1: len(rule_to_tokens) - 1]

    uri_to_tokens = uri.split('/')
    uri_to_tokens = uri_to_tokens[1: len(uri_to_tokens) - 1]

    for i in range(len(rule_to_tokens)):
        regex = r"^\{([\w_]+):(\bint|str|bool|float\b)\}$"
        if re.fullmatch(regex, rule_to_tokens[i]):
            groups = re.findall(regex, rule_to_tokens[i])
            var_name = groups[0][0]
            var_type = groups[0][1]
            if var_type == 'int':
                param[var_name] = int(uri_to_tokens[i])
            elif var_type == 'str':
                param[var_name] = str(uri_to_tokens[i])
            elif var_type == 'bool':
                param[var_name] = bool(uri_to_tokens[i])
            elif var_type == 'float':
                param[var_name] = float(uri_to_tokens[i])
    return param
