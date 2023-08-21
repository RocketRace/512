import abc
import ctypes
import enum
import functools
import operator
import random
import sys

'''
PYSP
PYthon String Programming

lisplike language built on Python

nil = ... or Ø
nil () -> 0
n: nat () -> succ n
nil (nil) -> []
l: list (x: any) -> l + [x]
n: nat (node) -> n <latch node to field n>
n: nat (list) -> any <hatch node in field n with msgs>
l: list () -> l + msgs()

field 0 is reserved to root node
field 1 is reserved to trunk node

root & trunk node:
- takes 2+ messages
- 1st message is leaf (nat)
- 2nd message is bug (nat)
- more optional msgs based on op

root node:
	0: ops:
		0: =
		1: !!
		2: !
	1: nat:
		0: +
		1: -
		2: *
		3: /
		4: ^
		5: %
		6: <
		7: >
	2: list:
		0: [x]
		1: [x:y]
		2: len
		3: +
		4: sum
	3: flow
		0: if
		1: wrap
		2: ()
		3: expand msgs
	4: ffi
		0: get
		1: set
		2: !
		3: fn
		4: input
		5: print
trunk node:
	0: rat:
		0: nat->
		1: ->nat
	1: seq:
		0: ~
		1: map
		2: filter
		3: *
	2: rand:
		0: ?
		1: range
		2: choiche
		3: ?!
	3: c:
		0: run gcc
		1: run clanc
	4: extra:
		0: sbstr
		1: b32e
'''

class Block:
	def __init__(self, label): 
		pass
	def __enter__(self):
		pass
	def __exit__(self, *args):
		pass

with Block('PYSP set-up'):
	with Block('Constants'):
		USE_SAFE_SENTINEL = False
		NIL_STR = 'Ø' if USE_SAFE_SENTINEL else '...'
	
	with Block('PYSP Types'):
		class Base:
			__slots__ = ()
			nil_str = NIL_STR
			def __repr__(self):
				return f'({self.__class__.__name__} at {id(self):x})'

		class Nil(Base):
			__slots__ = ()
			def __call__(self, msg = None):
				if msg is None:
					return Nat(0)
				elif isinstance(msg, Nil):
					return List([])
				else:
					raise TypeError(f'Message to Nil must be Nil, not {msg!r}')
			def __init__(self, nil = None):
				pass
			def __eq__(self, other):
				return isinstance(other, Nil)
			def __str__(self):
				return self.nil_str
			def __hash__(self):
				return hash(None)

		class Nat(Base):
			__slots__ = 'value',
			def __init__(self, value):
				self.value = int(value)
			def __call__(self, message = None):
				if message is None:
					return +self
				elif isinstance(message, (str, NodeBase)):
					state_node_field[~self] = to_node(message)
					return self
				elif isinstance(message, List):
					state_priv_msgs[:] = message
					return state_node_field[~self].do()
				else:
					raise TypeError(f'Message to Nat must be Node or List, not {message!r}')
			def __pos__(self):
				return Nat(~self + 1)
			def __invert__(self):
				return self.value
			def __repr__(self):
				return f'({self.__class__.__name__} {self.value} at {id(self):x})'
			def __str__(self):
				return str(~self)
			def __eq__(self, other):
				if not isinstance(other, Nat):
					return False
				return ~self == ~other
			def __lt__(self, other):
				return ~self < ~other
			def __gt__(self, other):
				return ~self > ~other
			def __hash__(self):
				return hash(~self)

		class List(Base):
			__slots__ = 'view',
			def __init__(self, view):
				self.view = view
			def __call__(self, msg = None):
				if msg is None:
					self ^ state_priv_msgs[:]
				elif isinstance(msg, str):
					self <<= Node(msg)
				else:
					self <<= msg
				return self
			def double(self):
				return type(self)([
					x.double() if isinstance(x, List) else x for x in self
				])
			def __invert__(self):
				return self.view
			def __ilshift__(self, other):
				(~self).append(other)
				return self
			def __xor__(self, other):
				(~self).extend(~other)
			def __str__(self):
				return '(' + ', '.join(str(value) for value in ~self) + ')'
			def __len__(self):
				return len(~self)
			def __iter__(self):
				return iter(~self)
			def __eq__(self, other):
				if not isinstance(other, List):
					return False
				return all(x == y for x, y in zip(self, other))

		class NodeBase(Base):
			__slots__ = ()
			@abc.abstractmethod
			def do(self): 
				pass

		def to_node(into):
			if isinstance(into, str):
				return Node(into)
			return into

		class Node(NodeBase):
			__slots__ = 'raw', 'compiled'
			def __init__(self, raw):
				try:
					self.raw = raw
					self.compiled = compile(raw, filename='(Node)', mode='eval')
				except SyntaxError as e:
					raise SyntaxError('Node must contain valid source code') from e
			def __str__(self):
				return f'\'{self.raw}\''
			def do(self):
				return eval(self.compiled)
			def __eq__(self, other):
				if not isinstance(other, Node):
					return False
				return self.raw == other.raw

		class CoreNode(NodeBase):
			__slots__ = 'fn',
			def do(self):
				return self.fn()
			def __init__(self, fn):
				self.fn = fn
	
	with Block('Core Nodes'):
		with Block('Core Node set-up'):
			def get_msgs(min, max = None):
				msg_count = len(state_priv_msgs[:])
				if msg_count < min:
					raise TypeError(f'Root Core node takes at least {min} messages, got {msg_count}')
				if max is not None and msg_count > max:
					raise TypeError(f'Root Core node takes at most {max} messages, got {msg_count}')
				return state_priv_msgs[:]

			def do_core_node(root = True):
				first_msg, second_msg, *other_msgs = get_msgs(2)
				if not isinstance(first_msg, Nat):
					raise TypeError(f'Core node takes Nat as first message, got {first_msg!r}')
				if not isinstance(second_msg, Nat):
					raise TypeError(f'Core node takes Nat as second message, got {second_msg!r}')
				try:
					if root:
						return root_leaves[~first_msg][~second_msg](*other_msgs)
					else:
						return trunk_leaves[~first_msg][~second_msg](*other_msgs)
				except IndexError as e:
					raise ValueError(f'Value too large ({first_msg!r}), maximum is {len(trunk_leaves) - 1}') from e
				# except TypeError as e:
				# 	raise TypeError(f'Wrong number ({len(other_msgs)}) of messages given to leaf (or it could just be an error raised above)') from e

			@CoreNode
			def root_core_node():
				return do_core_node()

			@CoreNode
			def trunk_core_node():
				return do_core_node(root=False)
		
		with Block('Core Node Leaf set-up'):
			def wrap_bin_args(l_wrap, r_wrap):
				def inner(bug):
					def innerer(left, right):
						return bug(l_wrap(left), r_wrap(right))
					return innerer
				return inner

			def wrap_both_bin_args(wrap):
				return wrap_bin_args(wrap, wrap)
			
			def wrap_all_args(wrap):
				def inner(bug):
					def innerer(*msgs):
						return bug(*(wrap(msg) for msg in msgs))
					return innerer
				return inner

			def wrap_return(wrap):
				def inner(bug):
					def innerer(*msgs):
						return wrap(bug(*msgs))
					return innerer
				return inner

			def else_bin_op(op):
				def inner(bug):
					def innerer(l_msg, r_msg):
						value = bug(l_msg, r_msg)
						if value is not None:
							return value
						return op(l_msg, r_msg)
					return innerer
				return inner

			def unwrap_nat(msg):
				if not isinstance(msg, Nat):
					raise TypeError(f'Message given must be nat, not {msg}')
				return ~msg

			def nat_bin_op(op):
				def inner(bug):
					x = wrap_return(Nat)(wrap_both_bin_args(unwrap_nat)(else_bin_op(op)(bug)))
					return x
				return inner

			class LeafMeta(type):
				def __new__(mcls, name, bases, ns, *, abstract = False, root = True):
					if not abstract:
						for bug in ns.values():
							if callable(bug):
								if root:
									root_leaves[RootLeaves[name.lower().removesuffix('leaf')]].append(bug)
								else:
									trunk_leaves[TrunkLeaves[name.lower().removesuffix('leaf')]].append(bug)
					return super().__new__(mcls, name, bases, {})
		
		with Block('Root Core Node Leaves'):
			class RootBase(metaclass=LeafMeta, abstract=True):
				pass

			class RootLeaves(enum.IntEnum):
				ops = 0
				nat = 1
				list = 2
				flow = 3
				ffi = 4

			root_leaves= [[] for _ in RootLeaves]

			def pysp_bool(py_bool):
				if py_bool:
					return Nat(0)
				else:
					return Nil()

			class OpsLeaf(RootBase):
				@wrap_return(pysp_bool)
				@else_bin_op(operator.eq)
				def equality(left, right):
					pass
				
				@wrap_return(pysp_bool)
				def truthy(msg):
					return not isinstance(msg, Nil)

				@wrap_return(pysp_bool)
				def un_truthy(msg):
					return isinstance(msg, Nil)

			class NatLeaf(RootBase):
				@wrap_return(Nat)
				@wrap_all_args(unwrap_nat)
				def add(*nats):
					return sum(nats)

				@nat_bin_op(operator.sub)
				def subtract(l_nat, r_nat):
					if l_nat < r_nat:
						return 0

				@wrap_return(Nat)
				@wrap_all_args(unwrap_nat)
				def multiply(*nats):
					return functools.reduce(operator.mul, nats)

				@nat_bin_op(operator.floordiv)
				def divide(l_nat, r_nat):
					if r_nat == 0:
						raise ZeroDivisionError('Second message is zero Nat')

				@nat_bin_op(operator.mod)
				def modulos(l_nat, r_nat):
					if r_nat == 0:
						raise ZeroDivisionError('Second message is zero Nat')
				
				@nat_bin_op(operator.pow)
				def exponentiate(l_nat, r_nat):
					pass
				
				@wrap_return(pysp_bool)
				@else_bin_op(operator.lt)
				def less_than(l_nat, r_nat):
					pass
				
				@wrap_return(pysp_bool)
				@else_bin_op(operator.gt)
				def greater_than(l_nat, r_nat):
					pass
			
			class ListLeaf(RootBase):
				def sli(pysp_list, nat_idx):
					try:
						return (~pysp_list)[~nat_idx]
					except IndexError as e:
						raise ValueError('Index out of bounds') from e
				
				@wrap_return(List)
				def slice(pysp_list, start_idx, end_idx):
					try:
						return (~pysp_list)[~start_idx:end_idx]
					except IndexError as e:
						raise ValueError('Index out of bounds') from e

				@wrap_return(Nat)
				def length(pysp_list):
					return len(pysp_list)
				
				@wrap_return(List)
				def join(left, right):
					return ~left + ~right
				
				@wrap_return(List)
				def join2(pysp_lists):
					return functools.reduce(operator.add, [~x for x in pysp_lists], [])

			class FlowLeaf(RootBase):
				def if_elsif(cond_msg, *eq_node_pairs):
					for case_val, case_node in zip(eq_node_pairs[::2], eq_node_pairs[1::2]):
						if cond_msg == case_val:
							return case_node.do()
					if len(eq_node_pairs) & 1:
						return eq_node_pairs[-1].do()
					else:
						return cond_msg

				@wrap_return(CoreNode)
				def wrap(msg):
					def inner():
						return msg
					return inner

				@wrap_return(CoreNode)
				def call(nat_ptr, msgs):
					def inner():
						return nat_ptr(msgs)
					return inner
				
				@wrap_return(CoreNode)
				def expand(nat_ptr, node):
					def wrapper(x):
						return x
					def inner():
						for i, msg in enumerate(get_msgs(0)):
							Nat(~nat_ptr + i)(CoreNode(functools.partial(wrapper, msg)))
						return node.do()
					return inner

			with Block('FFI'):
				with Block('FFI set-up'):
					class PyObject(Base):
						@abc.abstractclassmethod
						def from_py(cls, py_obj): pass
						@abc.abstractclassmethod
						def from_pysp(cls, pysp_obj): pass
						@abc.abstractmethod
						def to_py(self): pass

					def py_to_ffi(py_obj):
						py_ffi_mapping = [
							(type(None), PyNone),
							(int, PyInt),
							(list, PyList),
							(bytes, PyBytes),
							(str, PyString),
							(type(lambda: 0), PyLambda),
						]
						for py_t, ffi_t in py_ffi_mapping:
							if isinstance(py_obj, py_t):
								return ffi_t.from_py(py_obj)
						raise TypeError('No basic ffi representation found')

					def pysp_to_ffi(pysp_obj):
						if isinstance(pysp_obj, PyObject):
							return pysp_obj
						if isinstance(pysp_obj, Nil):
							return PyNone.from_pysp(pysp_obj)
						if isinstance(pysp_obj, Nat):
							return PyInt.from_pysp(pysp_obj)
						if isinstance(pysp_obj, List):
							header = (~pysp_obj)[0]
							if header == Nat(0):
								return PyList.from_pysp(pysp_obj)
							elif header == Nat(1):
								return PyBytes.from_pysp(pysp_obj)
							elif header == Nat(2):
								return PyString.from_pysp(pysp_obj)
							else:
								raise TypeError('List header not recognized')
						raise TypeError('No basic ffi representation found')

					class PyNone(Nil, PyObject):
						@classmethod
						def from_py(cls, py_none):
							return Nil()
						@classmethod
						def from_pysp(cls, nil):
							return PyNone()
						def to_py(self):
							return None

					class PyInt(Nat, PyObject):
						@classmethod
						def from_py(cls, py_int):
							if py_int < 0:
								raise TypeError('Nat can only take nonnegative ints')
							return cls(py_int)
						@classmethod
						def from_pysp(cls, nat):
							return cls(~nat)
						def to_py(self):
							return ~self
					
					class PyList(List, PyObject):
						@classmethod
						def from_py(cls, py_list):
							return cls([Nat(0)] + [py_to_ffi(x) for x in py_list])
						@classmethod
						def from_pysp(cls, pysp_list):
							return cls(~pysp_list)
						def to_py(self):
							return [pysp_to_ffi(x).to_py() for x in (~self)[1:]]

					class PyBytes(List, PyObject):
						@classmethod
						def from_py(cls, py_bytes):
							return cls([Nat(1)] + [Nat(c) for c in py_bytes])
						@classmethod
						def from_pysp(cls, pysp_list):
							return cls(~pysp_list)
						def to_py(self):
							temp = []
							for nat in (~self)[1:]:
								if not isinstance(nat, Nat):
									raise TypeError('PyString is a List of Nats')
								temp.append(bytes([~nat]))
							return b''.join(temp)

					class PyString(List, PyObject):
						@classmethod
						def from_py(cls, py_str):
							return cls([Nat(2)] + [Nat(ord(c)) for c in py_str])
						@classmethod
						def from_pysp(cls, pysp_list):
							return cls(~pysp_list)
						def to_py(self):
							temp = []
							for nat in (~self)[1:]:
								if not isinstance(nat, Nat):
									raise TypeError('PyString is a List of Nats')
								temp.append(chr(~nat))
							return ''.join(temp)
					
					class PyLambda(PyObject):
						__slots__ = 'fn',
						@classmethod
						def from_py(cls, py_fn):
							return cls(py_fn)
						def __init__(self, fn):
							self.fn = fn
						@classmethod
						def from_pysp(cls, node):
							raise TypeError('Internal compiler error: attempted to unwrap an Err value')
						def to_py(self):
							return self.fn

				class FfiLeaf(RootBase):
					def py_name(name):
						name_str = PyString(~name)
						return py_to_ffi(globals()[name_str.to_py()])

					@wrap_return(Nil)
					def py_define(name, value):
						name_str = PyString.from_pysp(name)
						globals()[name_str.to_py()] = pysp_to_ffi(value).to_py()
					
					def py_panic(err_code):
						raise Exception(~err_code)

					def py_lambda(node):
						@PyLambda
						def inner(*py_args):
							state_priv_msgs[:] = List([py_to_ffi(py_arg) for py_arg in py_args])
							return pysp_to_ffi(node.do()).to_py()
						return inner
					
					def py_out(pysp_str):
						return Nat(sys.stdout.write(pysp_to_ffi(pysp_str).to_py()))
					
					def py_in(pysp_nat):
						return py_to_ffi(sys.stdout.read(~pysp_nat))

		with Block('Trunk Core Node Leaves'):
			class TrunkMeta(LeafMeta):
				def __new__(mcls, name, bases, ns, *, abstract = False, root = False):
					return super().__new__(mcls, name, bases, ns, abstract=abstract, root=root)

			class TrunkBase(metaclass=TrunkMeta, abstract=True):
				pass

			class TrunkLeaves(enum.IntEnum):
				rat = 0
				seq = 1
				rand = 2
				c = 3
				extra = 4

			trunk_leaves = [[] for _ in TrunkLeaves]

			def do_root(leaf, bug, *msgs):
				return Nat(0)(List([Nat(leaf), Nat(bug), *msgs]))

			class RatLeaf(TrunkBase):
				def from_nat(nat):
					return List([Nil(), nat, Nat(1)])
				
				def to_nat(rat):
					return do_root(1, 3, do_root(2, 0, rat, Nat(1)), do_root(2, 0, rat, Nat(2)))

			class SeqLeaf(TrunkBase):
				def reverse(pysp_list):
					return List(reversed(~pysp_list))
				
				def map(node, pysp_list):
					x = []
					for elem in pysp_list:
						state_priv_msgs[:] = List([elem])
						x.append(node.do())
					return List(x)
				
				def filter(node, pysp_list):
					x = []
					for elem in pysp_list:
						state_priv_msgs[:] = List([elem])
						if not isinstance(node.do(), Nil):
							x.append(elem)
					return List(x)

				def repeat(msg, nat):
					return List([msg for _ in range(~nat)])
			
			class RandLeaf(TrunkBase):
				def rand():
					if random.random() > 0.5:
						return Nil()
					return Nat()

				@wrap_return(Nat)
				def rand_nat(left_nat, right_nat):
					return random.randint(~left_nat, ~right_nat)

				def rand_elems(pysp_list, nat):
					return random.choices(~pysp_list, k=~nat)

				def rand_panic():
					if random.random() > 0.5:
						raise Exception(-1)
					return Nil()
			
			class CLeaf(TrunkBase):
				def gcc(node):
					return None

				def clang(node):
					pass

			class ExtraLeaf(TrunkBase):
				def rep_substring(str_list, chr_nat, count_nat):
					...

				def b32e(str_list):
					return

		with Block('Root & Trunk Core Node wrap-up'):
			class Wrapper:
				def __init__(self, wrapped):
					self[:] = wrapped
				def __getitem__(self, _):
					return self.wrapped.double()
				def __setitem__(self, _, wrapped):
					self.wrapped = wrapped.double()

			state_priv_msgs = Wrapper(List([]))
			state_node_field  = { 0: root_core_node, 1: trunk_core_node }
	
	with Block('Wrap-up'):
		if USE_SAFE_SENTINEL:
			Ø = Nil()
		else:
			ctypes.py_object.from_address(id(...) + 8).value = Nil

with Block('Tests'):
	def test(s):
		import base64
		return base64.b32encode(s.encode()).decode('utf-8')

	def check(s):
		assert test(s) == entry(s)

with Block('Code'):
	...(...)(...()(...(...)(...()()()()())(...()())(...(...)(...()()())(...()(...(...)(...()())(...()()()()()())(...()()()()()()()()()()())(...()()()))())(...()(...(...)(...()())(...()()())(...()()())(...()()()()()())(...()()()()()()()()()()()())))(...()(...(...)(...()())(...()()())(...()()()()())(...()()()()())(...()()()()()()()()))()()()())(...()(...(...)(...()())(...()()())(...()()()()())(...()()()()())(...()()()()()()()()))()())(...()(...(...)(...()())(...()()()()()())(...()()()()()()()()()()()())(...()()()))))(...()(...(...)(...()()()()())(...())(...(...)(...()()())(...()(...(...)(...()())(...()()())(...()()()()())(...()()()()())(...()()()()()()()()))()()()())(...()(...(...)(...()())(...()()()()()())(...()()()()()()()()()()())(...()()()))())(...()(...(...)(...()())(...()()())(...()()()()())(...()()()()())(...()()()()()()()()))()()())(...()(...(...)(...()())(...()()())(...()()()()())(...()()()()())(...()()()()()()()()))()()()()))))))(...()(...(...)(...()()()()())(...()()()()())(...()(...(...)(...()()())(...()()()())(...(...)(...()()()))(...()(...(...)(...()()())(...()()()()())(...()()(...(...)(...()())(...()()()())(...(...)(...()(...(...)(...()())(...()()())(...()()()()())(...()()()()())(...()()()()()()()))())(...()(...(...)(...()())(...()()())(...()()()()())(...()()()())(...()()()())(...()()()()))())(...()(...(...)(...()())(...()()())(...()()()()())(...()()()())(...()()()())(...()()()()))()()())(...()(...(...)(...()())(...()()()()()())(...()()()()()()()()()()())(...()()()))()()())(...()(...(...)(...()())(...()()())(...()()()()())(...()()()()())(...()()()()()()()()))()()()()())(...()(...(...)(...()())(...()()())(...()()()()())(...()()()()())(...()()()()()()()()))()()())(...()()()()()()()()()()()))(...()()()()()()()()()()())))))))))
