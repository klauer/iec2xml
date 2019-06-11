import re
from pyPEG import keyword

def iec_source(): return -1, [_library_element_declaration, action]
def _library_element_declaration(): return [data_type_declaration, function_declaration, function_block_declaration, program_declaration, configuration_declaration, global_var_declarations]
def letter(): return re.compile(r"[A-Za-z]")
def digit(): return re.compile(r"[0-9]")
def octal_digit(): return re.compile(r"[0-7]")
def hex_digit(): return re.compile(r"[0-9A-F]")
def _identifier(): return re.compile(r"\w+")
def _constant(): return [time_literal, _numeric_literal, _character_string, bit_string_literal, boolean_literal]
def _numeric_literal(): return [real_literal, integer_literal]
def integer_literal(): return (0, (integer_type_name, '#'), re.compile(r"(2\#(1|0)(_?(1|0))*)|(8\#[0-7](_?[0-7])*)|(16\#[0-9A-F](_?[0-9A-F])*)|((\+|\-)?[0-9](_?[0-9])*)"))
def signed_integer(): return re.compile(r"(\+|\-)?[0-9](_?[0-9])*")
def integer(): return re.compile(r"[0-9](_?[0-9])*")
def binary_integer(): return ('2#', re.compile(r"(1|0)(_?(1|0))*"))
def bit(): return re.compile(r"1|0")
def octal_integer(): return ('8#', re.compile(r"[0-7](_?[0-7])*"))
def hex_integer(): return ('16#', re.compile(r"[0-9A-F](_?[0-9A-F])*"))
def real_literal(): return [(0, (real_type_name, '#'), re.compile(r"((\+|\-)?[0-9](_?[0-9])*)\.([0-9](_?[0-9])*)((e|E)(\+|\-)?([0-9](_?[0-9])*))?")), (0, (real_type_name, '#'), re.compile(r"((\+|\-)?[0-9](_?[0-9])*)((e|E)(\+|\-)?([0-9](_?[0-9])*))"))]
def exponent(): return re.compile(r"(E|e)(\+|\-)?[0-9](_?[0-9])*")
def bit_string_literal(): return (0, (bit_string_type_name, '#'), re.compile(r"(2\#(1|0)(_?(1|0))*)|(8\#[0-7](_?[0-7])*)|(16\#[0-9A-F](_?[0-9A-F])*)|([0-9](_?[0-9])*)"))
def boolean_literal(): return (0, 'BOOL#', re.compile(r"1|0|TRUE|FALSE"))
def _character_string(): return [single_byte_character_string, double_byte_character_string]
def single_byte_character_string(): return re.compile(r"\'([^\$\"\']|\$\$|\$L|\$N|\$P|\$R|\$T|\$l|\$n|\$p|\$r|\$t|\$\'|\"|\$[0-9A-F][0-9A-F])*\'")
def double_byte_character_string(): return re.compile(r"\"([^\$\"\']|\$\$|\$L|\$N|\$P|\$R|\$T|\$l|\$n|\$p|\$r|\$t|\$\'|\"|\$[0-9A-F][0-9A-F][0-9A-F][0-9A-F])*\"")
def single_byte_character_representation(): return re.compile(r"[^\$\"\']|\$\$|\$L|\$N|\$P|\$R|\$T|\$l|\$n|\$p|\$r|\$t|\$\'|\"|\$[0-9A-F][0-9A-F]")
def double_byte_character_representation(): return re.compile(r"[^\$\"\']|\$\$|\$L|\$N|\$P|\$R|\$T|\$l|\$n|\$p|\$r|\$t|\$\'|\"|\$[0-9A-F][0-9A-F][0-9A-F][0-9A-F]")
def common_character_representation(): return re.compile(r"[^\$\"\']|\$\$|\$L|\$N|\$P|\$R|\$T|\$l|\$n|\$p|\$r|\$t")
def time_literal(): return [duration, time_of_day, date, date_and_time]
def duration(): return (['TIME', 'T', 't'], '#', 0, '-', _interval)
def _interval(): return [days, hours, minutes, seconds, milliseconds]
def days(): return [(fixed_point, 'd'), (integer, 'd', 0, '_', hours), (integer, 'd')]
def fixed_point(): return re.compile(r"[0-9](_?[0-9])*\.[0-9](_?[0-9])*")
def hours(): return [(fixed_point, 'h'), (integer, 'h', 0, '_', minutes), (integer, 'h')]
def minutes(): return [(fixed_point, 'm'), ((integer, 'm', 0, '_', seconds), (integer, 'm'))]
def seconds(): return [(fixed_point, 's'), (integer, 's', 0, '_', milliseconds), (integer, 's')]
def milliseconds(): return [(fixed_point, 'ms'), (integer, 'ms')]
def time_of_day(): return (['TIME_OF_DAY', 'TOD'], '#', _daytime)
def _daytime(): return (day_hour, ':', day_minute, ':', day_second)
def day_hour(): return integer
def day_minute(): return integer
def day_second(): return fixed_point
def date(): return (['DATE', 'D', 'd'], '#', date_literal)
def date_literal(): return (year, '-', month, '-', day)
def year(): return integer
def month(): return integer
def day(): return integer
def date_and_time(): return (['DATE_AND_TIME', 'DT'], '#', date_literal, '-', _daytime)
def data_type_name(): return [non_generic_type_name, generic_type_name]
def non_generic_type_name(): return (0, pointer_to, [_elementary_type_name, derived_type_name])
def _elementary_type_name(): return [_numeric_type_name, date_type_name, bit_string_type_name, string_type_declaration]
def _numeric_type_name(): return [integer_type_name, real_type_name]
def integer_type_name(): return [_signed_integer_type_name, _unsigned_integer_type_name]
def type_sint(): return keyword('SINT')
def type_int(): return keyword('INT')
def type_dint(): return keyword('DINT')
def type_lint(): return keyword('LINT')
def _signed_integer_type_name(): return [type_sint, type_int, type_dint, type_lint]
def type_usint(): return keyword('USINT')
def type_uint(): return keyword('UINT')
def type_udint(): return keyword('UDINT')
def type_ulint(): return keyword('ULINT')
def _unsigned_integer_type_name(): return [type_usint, type_uint, type_udint, type_ulint]
def type_real(): return keyword('REAL')
def type_lreal(): return keyword('LREAL')
def real_type_name(): return [type_real, type_lreal]
def type_tod(): return [keyword('TIME_OF_DAY'), keyword('TOD')]
def type_datetime(): return [keyword('DATE_AND_TIME'), keyword('DT')]
def type_date(): return keyword('DATE')
def type_time(): return keyword('TIME')
def date_type_name(): return [type_tod, type_datetime, type_date, type_time]
def type_bool(): return keyword('BOOL')
def type_byte(): return keyword('BYTE')
def type_word(): return keyword('WORD')
def type_dword(): return keyword('DWORD')
def type_lword(): return keyword('LWORD')
def bit_string_type_name(): return [type_bool, type_byte, type_word, type_dword, type_lword]
def generic_type_name(): return re.compile(r"ANY|ANY_DERIVED|ANY_ELEMENTARY|ANY_MAGNITUDE|ANY_NUM|ANY_REAL|ANY_INT|ANY_BIT|ANY_STRING|ANY_DATE")
def derived_type_name(): return [single_element_type_name, array_type_name, structure_type_name, string_type_name]
def single_element_type_name(): return [simple_type_name, subrange_type_name, enumerated_type_name]
def simple_type_name(): return _identifier
def subrange_type_name(): return _identifier
def enumerated_type_name(): return _identifier
def array_type_name(): return _identifier
def structure_type_name(): return _identifier
def data_type_declaration(): return (keyword('TYPE'), -1, _type_declaration, keyword('END_TYPE'), 0, ';')
def pointer_to(): return (keyword('POINTER'), keyword('TO'))
def _type_declaration(): return [(array_type_declaration, ';'), (structure_type_declaration, 0, ';'), (string_type_declaration, ';'), (_single_element_type_declaration, ';')]
def _single_element_type_declaration(): return [simple_type_declaration, subrange_type_declaration, enumerated_type_declaration]
def simple_type_declaration(): return (simple_type_name, ':', simple_spec_init)
def simple_spec_init(): return (0, pointer_to, _simple_specification, 0, (':=', expression))
def _simple_specification(): return [_elementary_type_name, simple_type_name]
def subrange_type_declaration(): return (subrange_type_name, ':', subrange_spec_init)
def subrange_spec_init(): return (0, pointer_to, subrange_specification, 0, (':=', expression))
def subrange_specification(): return [(integer_type_name, '(', subrange, ')'), subrange_type_name]
def subrange(): return (expression, '..', expression)
def enumerated_type_declaration(): return (enumerated_type_name, ':', enumerated_spec_init)
def enumerated_spec_init(): return (0, pointer_to, enumerated_specification, 0, (':=', enumerated_value))
def enumerated_specification(): return [('(', enumerated_value, -1, (',', enumerated_value), ')'), enumerated_type_name]
def enumerated_value(): return (0, (enumerated_type_name, '#'), _identifier, 0, (':=', integer_literal))
def array_type_declaration(): return (array_type_name, ':', array_spec_init)
def array_spec_init(): return (0, pointer_to, array_specification, 0, (':=', array_initialization))
def array_specification(): return (keyword('ARRAY'), '[', subrange, -1, (',', subrange), ']', keyword('OF'), [string_type, non_generic_type_name])
def array_initialization(): return [('[', array_initial_elements, -1, (',', array_initial_elements), ']'), (array_initial_elements, -1, (',', array_initial_elements))]
def array_initial_elements(): return [[([integer, enumerated_value], '(', 0, array_initial_element, ')'), _constant], array_initial_element]
def array_initial_element(): return [_constant, structure_initialization, enumerated_value]
def structure_type_declaration(): return (structure_type_name, ':', _structure_specification)
def _structure_specification(): return [(0, pointer_to, _structure_declaration), initialized_structure]
def initialized_structure(): return (structure_type_name, ':=', structure_initialization)
def _structure_declaration(): return (keyword('STRUCT'), structure_element_declaration, ';', -1, (structure_element_declaration, ';'), keyword('END_STRUCT'), 0, ';')
def structure_element_declaration(): return (structure_element_name, ':', [initialized_structure, array_spec_init, string_var_type, simple_spec_init, subrange_spec_init, enumerated_spec_init])
def structure_element_name(): return _identifier
def structure_initialization(): return ('(', structure_element_initialization, -1, (',', structure_element_initialization), ')')
def structure_element_initialization(): return [_constant, (structure_element_name, ':=', [_constant, enumerated_value, array_initialization, structure_initialization])]
def string_type_name(): return _identifier
def string(): return keyword('STRING')
def wstring(): return keyword('WSTRING')
def string_initialization(): return (':=', _character_string)
def string_type_declaration(): return (string_type_name, ':', string_type, 0, string_initialization)
def string_type(): return ([string, wstring], 0, [('[', [integer, simple_type_name], ']'), ('(', [integer, simple_type_name], ')')])
def string_var_type(): return (string_type, 0, string_initialization)
def _variable(): return [direct_variable, _symbolic_variable]
def _symbolic_variable(): return [multi_element_variable, variable_name]
def variable_name(): return (_identifier, 0, dereferenced)
def direct_variable(): return ('%', location_prefix, 0, size_prefix, integer, -1, ('.', integer))
def location_prefix(): return re.compile(r"I|Q|M")
def size_prefix(): return re.compile(r"X|B|W|D|L")
def _subscript(): return expression
def subscript_list(): return ('[', _subscript, -1, (',', _subscript), ']')
def dereferenced(): return '^'
def field_selector(): return (0, dereferenced, '.', variable_name)
def multi_element_variable(): return (variable_name, [subscript_list, field_selector], -1, [subscript_list, field_selector])
def retain(): return keyword('RETAIN')
def non_retain(): return keyword('NON_RETAIN')
def input_declarations(): return (keyword('VAR_INPUT'), 0, [retain, non_retain], -1, (_input_declaration, ';'), keyword('END_VAR'), 0, ';')
def _input_declaration(): return [var_init_decl, edge_declaration]
def r_edge(): return keyword('R_EDGE')
def f_edge(): return keyword('F_EDGE')
def edge_declaration(): return (_var1_list, ':', keyword('BOOL'), [r_edge, f_edge])
def var_init_decl(): return [array_var_init_decl, structured_var_init_decl, string_var_declaration, _var1_init_decl, fb_name_decl]
def _var1_init_decl(): return (_var1_list, ':', [simple_spec_init, subrange_spec_init, enumerated_spec_init])
def _var1_list(): return (variable_name, 0, location, -1, (',', variable_name, 0, location))
def array_var_init_decl(): return (_var1_list, ':', array_spec_init)
def structured_var_init_decl(): return (_var1_list, ':', initialized_structure)
def fb_name_decl(): return (fb_name_list, ':', function_block_type_name, 0, (':=', structure_initialization))
def fb_name_list(): return (fb_name, -1, (',', fb_name))
def fb_name(): return _identifier
def output_declarations(): return (keyword('VAR_OUTPUT'), 0, [retain, non_retain], -1, (var_init_decl, ';'), keyword('END_VAR'), 0, ';')
def input_output_declarations(): return (keyword('VAR_IN_OUT'), -1, (var_init_decl, ';'), keyword('END_VAR'), 0, ';')
def var_declaration(): return [_temp_var_decl, fb_name_decl]
def _temp_var_decl(): return [_var1_declaration, array_var_declaration, structured_var_declaration, string_var_declaration]
def _var1_declaration(): return (_var1_list, ':', [_simple_specification, subrange_specification, enumerated_specification])
def array_var_declaration(): return (_var1_list, ':', array_specification)
def structured_var_declaration(): return (_var1_list, ':', structure_type_name)
def var_declarations(): return (keyword('VAR'), 0, constant, -1, (var_init_decl, ';'), keyword('END_VAR'), 0, ';')
def retentive_var_declarations(): return (keyword('VAR'), keyword('RETAIN'), -1, (var_init_decl, ';'), keyword('END_VAR'), 0, ';')
def constant(): return keyword('CONSTANT')
def located_var_declarations(): return (keyword('VAR'), 0, [constant, retain, non_retain], -1, (located_var_decl, ';'), keyword('END_VAR'), 0, ';')
def located_var_decl(): return (0, variable_name, location, ':', located_var_spec_init)
def external_var_declarations(): return (keyword('VAR_EXTERNAL'), 0, constant, -1, (external_declaration, ';'), keyword('END_VAR'), 0, ';')
def external_declaration(): return (global_var_name, ':', [_simple_specification, subrange_specification, enumerated_specification, array_specification, structure_type_name, function_block_type_name])
def global_var_name(): return _identifier
def persistent(): return keyword('PERSISTENT')
def global_var_declarations(): return (keyword('VAR_GLOBAL'), 0, [constant, retain], 0, persistent, -1, ([var_init_decl, global_var_decl], ';'), keyword('END_VAR'), 0, ';')
def global_var_decl(): return (global_var_spec, ':', 0, [located_var_spec_init, function_block_type_name])
def global_var_spec(): return [global_var_list, (0, global_var_name, location)]
def located_var_spec_init(): return [simple_spec_init, subrange_spec_init, enumerated_spec_init, array_spec_init, initialized_structure, single_byte_string_spec, double_byte_string_spec]
def location(): return (keyword('AT'), direct_variable)
def global_var_list(): return (global_var_name, -1, (',', global_var_name))
def string_var_declaration(): return [single_byte_string_var_declaration, double_byte_string_var_declaration]
def single_byte_string_var_declaration(): return (_var1_list, ':', single_byte_string_spec)
def single_byte_string_spec(): return (keyword('STRING'), 0, [('[', [integer, simple_type_name], ']'), ('(', [integer, simple_type_name], ')')], 0, (':=', single_byte_character_string))
def double_byte_string_var_declaration(): return (_var1_list, ':', double_byte_string_spec)
def double_byte_string_spec(): return (keyword('WSTRING'), 0, [('[', [integer, simple_type_name], ']'), ('(', [integer, simple_type_name], ')')], 0, (':=', double_byte_character_string))
def incompl_located_var_declarations(): return (keyword('VAR'), 0, [retain, non_retain], -1, (incompl_located_var_decl, ';'), keyword('END_VAR'), 0, ';')
def incompl_located_var_decl(): return (variable_name, incompl_location, ':', var_spec)
def incompl_location(): return (keyword('AT'), re.compile(r"\%(I|Q|M)\*"))
def string(): return keyword('STRING')
def wstring(): return keyword('WSTRING')
def var_spec(): return [_simple_specification, subrange_specification, enumerated_specification, array_specification, structure_type_name, (string, 0, ('[', integer, ']')), (wstring, 0, ('[', integer, ']'))]
def _function_name(): return derived_function_name
def derived_function_name(): return _identifier
def function_declaration(): return (keyword('FUNCTION'), derived_function_name, ':', [_elementary_type_name, derived_type_name], -1, [_io_var_declarations, function_var_decls], [function_body, unknown_in_function], keyword('END_FUNCTION'), 0, ';')
def _io_var_declarations(): return [input_declarations, output_declarations, input_output_declarations]
def function_var_decls(): return (keyword('VAR'), 0, constant, -1, (var_init_decl, ';'), keyword('END_VAR'), 0, ';')
def function_body(): return statement_list
def function_var_decl(): return [_var1_init_decl, array_var_init_decl, structured_var_init_decl, string_var_declaration]
def function_block_type_name(): return [standard_function_block_name, derived_function_block_name]
def standard_function_block_name(): return _identifier
def derived_function_block_name(): return _identifier
def function_block_declaration(): return ([keyword('FUNCTION_BLOCK'), keyword('FUNCTIONBLOCK')], derived_function_block_name, -1, [_io_var_declarations, _other_var_declarations], [function_block_body, unknown_in_function_block], [keyword('END_FUNCTION_BLOCK'), keyword('END_FUNCTIONBLOCK')], 0, ';')
def _other_var_declarations(): return [external_var_declarations, var_declarations, retentive_var_declarations, non_retentive_var_decls, temp_var_decls, incompl_located_var_declarations]
def temp_var_decls(): return (keyword('VAR_TEMP'), -1, (_temp_var_decl, ';'), keyword('END_VAR'), 0, ';')
def non_retentive_var_decls(): return (keyword('VAR'), keyword('NON_RETAIN'), -1, (var_init_decl, ';'), keyword('END_VAR'), 0, ';')
def function_block_body(): return [sequential_function_chart, statement_list]
def program_type_name(): return _identifier
def program_declaration(): return (keyword('PROGRAM'), program_type_name, -1, [_io_var_declarations, _other_var_declarations, located_var_declarations, program_access_decls], [function_block_body, unknown_in_program], keyword('END_PROGRAM'), 0, ';')
def program_access_decls(): return (keyword('VAR_ACCESS'), program_access_decl, ';', -1, (program_access_decl, ';'), keyword('END_VAR'), 0, ';')
def program_access_decl(): return (access_name, ':', symbolic_variable, ':', non_generic_type_name, 0, direction)
def unknown_in_step(): return re.compile(r"(?s).*?(?=END_STEP)")
def unknown_in_transition(): return re.compile(r"(?s).*?(?=END_TRANSITION)")
def unknown_in_action(): return re.compile(r"(?s).*?(?=END_ACTION)")
def unknown_in_program(): return re.compile(r"(?s).*?(?=END_PROGRAM)")
def unknown_in_function(): return re.compile(r"(?s).*?(?=END_FUNCTION)")
def unknown_in_function_block(): return re.compile(r"(?s).*?(?=END_FUNCTION_BLOCK)")
def sequential_function_chart(): return (sfc_network, -1, sfc_network)
def sfc_network(): return (initial_step, -1, [step, transition, action, entry_action, exit_action])
def initial_step(): return (keyword('INITIAL_STEP'), step_name, ':', [sequential_function_chart, statement_list, action_association, unknown_in_step], 0, ';', keyword('END_STEP'), 0, ';')
def step(): return (keyword('STEP'), step_name, ':', 0, [statement_list, action_association, sequential_function_chart, unknown_in_step], 0, ';', keyword('END_STEP'), 0, ';')
def step_name(): return _identifier
def action_association(): return (action_name, '(', 0, action_qualifier, -1, (',', indicator_name), ')')
def action_name(): return re.compile(r"(?!END_)(\w+)")
def action_qualifier(): return [re.compile(r"N|R|S|P|P0|P1"), (timed_qualifier, ',', action_time)]
def timed_qualifier(): return re.compile(r"L|D|SD|DS|SL")
def action_time(): return [duration, variable_name]
def indicator_name(): return variable_name
def transition(): return [(keyword('TRANSITION'), 0, ('(', keyword('PRIORITY'), ':=', integer, ')'), keyword('FROM'), steps, keyword('TO'), steps, transition_condition, keyword('END_TRANSITION'), 0, ';'), (keyword('TRANSITION'), 0, transition_name, 0, ('(', keyword('PRIORITY'), ':=', integer, ')'), keyword('FROM'), steps, keyword('TO'), steps, transition_condition, keyword('END_TRANSITION'), 0, ';')]
def transition_name(): return (0, logical_not, _identifier)
def steps(): return [step_name, ('(', step_name, -1, (',', step_name), ')')]
def transition_condition(): return (':=', [(expression, 0, ';', re.compile(r"(?=END_TRANSITION)")), unknown_in_transition])
def action(): return (keyword('ACTION'), action_name, ':', [function_block_body, unknown_in_action], keyword('END_ACTION'), 0, ';')
def entry_action(): return (keyword('ENTRY_ACTION'), [function_block_body, unknown_in_action], keyword('END_ACTION'), 0, ';')
def exit_action(): return (keyword('EXIT_ACTION'), [function_block_body, unknown_in_action], keyword('END_ACTION'), 0, ';')
def configuration_name(): return _identifier
def resource_type_name(): return _identifier
def configuration_declaration(): return (keyword('CONFIGURATION'), configuration_name, 0, global_var_declarations, [single_resource_declaration, (resource_declaration, -1, resource_declaration)], 0, access_declarations, 0, instance_specific_initializations, keyword('END_CONFIGURATION'), 0, ';')
def resource_declaration(): return (keyword('RESOURCE'), resource_name, keyword('ON'), resource_type_name, 0, global_var_declarations, single_resource_declaration, keyword('END_RESOURCE'), 0, ';')
def single_resource_declaration(): return (-1, (task_configuration, ';'), program_configuration, ';', -1, (program_configuration, ';'))
def resource_name(): return _identifier
def access_declarations(): return (keyword('VAR_ACCESS'), access_declaration, ';', -1, (access_declaration, ';'), keyword('END_VAR'), 0, ';')
def access_declaration(): return (access_name, ':', access_path, ':', non_generic_type_name, 0, direction)
def access_path(): return [(0, (resource_name, '.'), direct_variable), (0, (resource_name, '.'), 0, (program_name, '.'), -1, (fb_name, '.'), symbolic_variable)]
def global_var_reference(): return (0, (resource_name, '.'), global_var_name, 0, ('.', structure_element_name))
def access_name(): return _identifier
def program_output_reference(): return (program_name, '.', symbolic_variable)
def program_name(): return _identifier
def read_write(): return keyword('READ_WRITE')
def read_only(): return keyword('READ_ONLY')
def direction(): return [read_write, read_only]
def task_configuration(): return (keyword('TASK'), task_name, task_initialization)
def task_name(): return _identifier
def task_initialization(): return ('(', 0, (keyword('SINGLE'), ':=', data_source, ','), 0, (keyword('INTERVAL'), ':=', data_source, ','), keyword('PRIORITY'), ':=', integer, ')')
def data_source(): return [_constant, global_var_reference, program_output_reference, direct_variable]
def program_configuration(): return (keyword('PROGRAM'), 0, [retain, non_retain], program_name, 0, (keyword('WITH'), task_name), ':', program_type_name, 0, ('(', prog_conf_elements, ')'))
def prog_conf_elements(): return (prog_conf_element, -1, (',', prog_conf_element))
def prog_conf_element(): return [fb_task, prog_cnxn]
def fb_task(): return (fb_name, keyword('WITH'), task_name)
def prog_cnxn(): return [(symbolic_variable, ':=', prog_data_source), (symbolic_variable, '=>', data_sink)]
def prog_data_source(): return [_constant, enumerated_value, global_var_reference, direct_variable]
def data_sink(): return [global_var_reference, direct_variable]
def instance_specific_initializations(): return (keyword('VAR_CONFIG'), -1, (instance_specific_init, ';'), keyword('END_VAR'), 0, ';')
def instance_specific_init(): return (resource_name, '.', program_name, '.', -1, (fb_name, '.'), [(variable_name, 0, location, ':', located_var_spec_init), (fb_name, ':', function_block_type_name, ':=', structure_initialization)])
def instruction_list(): return (il_instruction, -1, il_instruction)
def il_instruction(): return (0, (label, ':'), 0, [il_simple_operation, il_expression, il_jump_operation, il_fb_call, il_formal_funct_call, _il_return_operator], re.compile(r"\s*$"))
def label(): return _identifier
def il_simple_operation(): return [(_il_simple_operator, 0, il_operand), (_function_name, 0, il_operand_list)]
def il_expression(): return (_il_expr_operator, '(', 0, il_operand, re.compile(r"\s*$"), 0, simple_instr_list, ')')
def il_jump_operation(): return (_il_jump_operator, label)
def il_fb_call(): return (_il_call_operator, fb_name, 0, ('(', [(re.compile(r"\s*$"), 0, il_param_list), 0, il_operand_list], ')'))
def il_formal_funct_call(): return (_function_name, '(', re.compile(r"\s*$"), 0, il_param_list, ')')
def il_operand(): return [constant, _variable, enumerated_value]
def il_operand_list(): return (il_operand, -1, (',', il_operand))
def simple_instr_list(): return (il_simple_instruction, -1, il_simple_instruction)
def il_simple_instruction(): return ([il_simple_operation, il_expression, il_formal_funct_call], re.compile(r"\s*$"))
def il_param_list(): return (-1, il_param_instruction, il_param_last_instruction)
def il_param_instruction(): return ([il_param_assignment, il_param_out_assignment], ',', re.compile(r"\s*$"))
def il_param_last_instruction(): return ([il_param_assignment, il_param_out_assignment], re.compile(r"\s*$"))
def il_param_assignment(): return (il_assign_operator, [il_operand, ('(', re.compile(r"\s*$"), simple_instr_list, ')')])
def il_param_out_assignment(): return (il_assign_out_operator, _variable)
def il_operator_ld(): return keyword('LD')
def il_operator_ldn(): return keyword('LDN')
def il_operator_st(): return keyword('ST')
def il_operator_stn(): return keyword('STN')
def il_operator_not(): return keyword('NOT')
def il_operator_s(): return keyword('S')
def il_operator_r(): return keyword('R')
def il_operator_s1(): return keyword('S1')
def il_operator_r1(): return keyword('R1')
def il_operator_clk(): return keyword('CLK')
def il_operator_cu(): return keyword('CU')
def il_operator_cd(): return keyword('CD')
def il_operator_pv(): return keyword('PV')
def il_operator_in(): return keyword('IN')
def il_operator_pt(): return keyword('PT')
def il_operator_andn(): return [keyword('ANDN'), keyword('&N')]
def il_operator_and(): return [keyword('AND'), '&']
def il_operator_or(): return keyword('OR')
def il_operator_xor(): return keyword('XOR')
def il_operator_orn(): return keyword('ORN')
def il_operator_xorn(): return keyword('XORN')
def il_operator_add(): return keyword('ADD')
def il_operator_sub(): return keyword('SUB')
def il_operator_mul(): return keyword('MUL')
def il_operator_div(): return keyword('DIV')
def il_operator_mod(): return keyword('MOD')
def il_operator_gt(): return keyword('GT')
def il_operator_ge(): return keyword('GE')
def il_operator_eq(): return keyword('EQ')
def il_operator_lt(): return keyword('LT')
def il_operator_le(): return keyword('LE')
def il_operator_ne(): return keyword('NE')
def _il_simple_operator(): return [il_operator_ld, il_operator_ldn, il_operator_st, il_operator_stn, il_operator_not, il_operator_s, il_operator_r, il_operator_s1, il_operator_r1, il_operator_clk, il_operator_cu, il_operator_cd, il_operator_pv, il_operator_in, il_operator_pt, _il_expr_operator]
def _il_expr_operator(): return [il_operator_andn, il_operator_and, il_operator_or, il_operator_xor, il_operator_orn, il_operator_xorn, il_operator_add, il_operator_sub, il_operator_mul, il_operator_div, il_operator_mod, il_operator_gt, il_operator_ge, il_operator_eq, il_operator_lt, il_operator_le, il_operator_ne]
def il_assign_operator(): return (variable_name, ':=')
def il_assign_out_operator(): return (0, il_operator_not, variable_name, '=>')
def il_operator_cal(): return keyword('CAL')
def il_operator_calc(): return keyword('CALC')
def il_operator_calcn(): return keyword('CALCN')
def _il_call_operator(): return [il_operator_cal, il_operator_calc, il_operator_calcn]
def il_operator_ret(): return keyword('RET')
def il_operator_retc(): return keyword('RETC')
def il_operator_retcn(): return keyword('RETCN')
def _il_return_operator(): return [il_operator_ret, il_operator_retc, il_operator_retcn]
def il_operator_jmp(): return keyword('JMP')
def il_operator_jmpc(): return keyword('JMPC')
def il_operator_jmp(): return keyword('JMPCN')
def _il_jump_operator(): return [il_operator_jmp, il_operator_jmpc, il_operator_jmpcn]
def logical_or(): return keyword('OR')
def logical_xor(): return keyword('XOR')
def logical_and(): return keyword('AND')
def logical_not(): return keyword('NOT')
def modulo(): return keyword('MOD')
def equals(): return '='
def equals_not(): return '<>'
def less_or_equal(): return '<='
def greater_or_equal(): return '>='
def less_than(): return '<'
def greater_than(): return '>'
def adding(): return '+'
def subtracting(): return '-'
def multiply_with(): return '*'
def divide_by(): return '/'
def elevated_by(): return '**'
def minus(): return "-"
def plus(): return "+"
def expression(): return (_xor_expression, -1, (logical_or, _xor_expression))
def _xor_expression(): return (_and_expression, -1, (logical_xor, _and_expression))
def _and_expression(): return (_comparison, -1, (logical_and, _comparison))
def _comparison(): return (_equ_expression, -1, ([equals, equals_not], _equ_expression))
def _equ_expression(): return (_add_expression, -1, ([less_or_equal, greater_or_equal, less_than, greater_than], _add_expression))
def _add_expression(): return (_term, -1, (_add_operator, _term))
def _add_operator(): return [adding, subtracting]
def _term(): return (_power_expression, -1, (_multiply_operator, _power_expression))
def _multiply_operator(): return [modulo, multiply_with, divide_by]
def _power_expression(): return (_unary_expression, -1, (elevated_by, _unary_expression))
def _unary_expression(): return [_constant, (0, _unary_operator, _primary_expression)]
def _unary_operator(): return [logical_not, minus, plus]
def function_call(): return (_function_name, '(', 0, (param_assignment, -1, (',', param_assignment)), ')')
def _primary_expression(): return [('(', expression, ')'), function_call, _variable]
def statement_list(): return (_statement, -1, _statement)
def _statement(): return [(';', -1, ';'), method, assignment_statement, _subprogram_control_statement, _selection_statement, _iteration_statement, (action_name, ';')]
def assignment_statement(): return (_variable, ':=', expression, ';')
def method(): return (expression, '(', ')', ';')
def return_statement(): return (keyword('RETURN'), 0, ';')
def _subprogram_control_statement(): return [return_statement, (fb_invocation, ';')]
def fb_invocation(): return (fb_name, '(', 0, (param_assignment, -1, (',', param_assignment)), ')')
def param_assignment(): return [(0, keyword('NOT'), variable_name, '=>', _variable), (0, (variable_name, ':='), expression)]
def _selection_statement(): return [if_statement, case_statement]
def if_statement(): return (keyword('IF'), expression, keyword('THEN'), statement_list, -1, (keyword('ELSIF'), expression, keyword('THEN'), statement_list), 0, (keyword('ELSE'), statement_list), keyword('END_IF'), 0, ';')
def case_statement(): return (keyword('CASE'), expression, keyword('OF'), case_element, -1, case_element, 0, (keyword('ELSE'), statement_list), keyword('END_CASE'), 0, ';')
def case_element(): return (case_list, ':', statement_list)
def case_list(): return (case_list_element, -1, (',', case_list_element))
def case_list_element(): return [subrange, integer_literal, enumerated_value]
def _iteration_statement(): return [for_statement, while_statement, repeat_statement, exit_statement]
def for_statement(): return (keyword('FOR'), control_variable, ':=', for_list, keyword('DO'), statement_list, keyword('END_FOR'), 0, ';')
def control_variable(): return _identifier
def for_list(): return (expression, keyword('TO'), expression, 0, (keyword('BY'), expression))
def while_statement(): return (keyword('WHILE'), expression, keyword('DO'), statement_list, keyword('END_WHILE'), 0, ';')
def repeat_statement(): return (keyword('REPEAT'), statement_list, keyword('UNTIL'), expression, keyword('END_REPEAT'), 0, ';')
def exit_statement(): return (keyword('EXIT'), 0, ';')
