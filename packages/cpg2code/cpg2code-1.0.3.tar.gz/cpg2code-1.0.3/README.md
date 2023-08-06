# EnhancedPHPJoern Framework Cpg2Code Library


## Introduction

This framework helps you convert code from CodePropertyGraph of PHP.

## Installation

### install from pip (not public yet)

```Bash
pip3 install cpg2code
```


### install from source code

```Bash
git clone 
python setup.py install
```


## Usage

```python
from enhanced_phpjoern_framework import Neo4jEngine
from enhanced_phpjoern_framework.graph_traversal import ControlGraphForwardTraversal
from cpg2code.cpg2code_factory import Cpg2CodeFactory
# WordPress-5.7.1/wp-load.php
neo4j_engine = Neo4jEngine.from_dict(NEO4J_DEFAULT_CONFIG)
traversal_entity = ControlGraphForwardTraversal(neo4j_engine)
file = neo4j_engine.get_file_name_belong_node('wp-load.php')
x = neo4j_engine.get_ast_child_node(neo4j_engine.get_ast_child_node(file))
origin = neo4j_engine.get_ast_root_node(x)
traversal_entity.origin = [origin]
traversal_entity.run()
rec = traversal_entity.get_record()  # type:nx.DiGraph
rec_list = [k for k, p in rec.nodes.items()]
result = Cpg2CodeFactory.extract_code(neo4j_engine, rec_list)
print(result)
```

The compare of result can be seen as follows(the left is the source file and the right is the generated file)

![http://github.com/ninthDevilHAUNSTER/cpg2code/raw/master/example/result_cmp.png](result_cmp)
## Changelog

See `[CHANGES.md](https://github.com/ninthDevilHAUNSTER/code2cpg/blob/master/CHANGES.md)`

## Authors

See `[AUTHORS.md](https://github.com/ninthDevilHAUNSTER/code2cpg/blob/master/AUTHORS.md)`

## License

See `[LICENSE.txt](https://github.com/ninthDevilHAUNSTER/code2cpg/blob/master/LICENSE.txt)`



