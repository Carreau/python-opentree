#!/usr/bin/env python3
import sys
import json
from opentree import OTCommandLineTool, process_ott_id_and_node_id_args


cli = OTCommandLineTool(usage='Display node info for the synthetic tree node(s) requested',
                        add_ott_ids_arg=True,
                        add_node_ids_arg=True)
cli.parser.add_argument('--include-lineage', action='store_true',
                        help='Return the lineage of nodes back to the root of the tree')
OT, args = cli.parse_cli()


ott_id_list, node_id_list = process_ott_id_and_node_id_args(args)
# use node_id_list if there are multiple. This is an odd call in the API
if (not node_id_list) and (not ott_id_list):
    sys.exit('Either --node-ids or --ott-ids must be provided.\n')
if len(ott_id_list) > 1 or (node_id_list and ott_id_list):
    node_id_list.extend(['ott{}'.format(i) for i in ott_id_list])
    ott_id_list.clear()


if len(node_id_list) == 1:
    output = OT.synth_node_info(node_id=node_id_list[0], include_lineage=args.include_lineage)
elif len(node_id_list) > 1:
    output = OT.synth_node_info(node_ids=node_id_list, include_lineage=args.include_lineage)
else:
    assert len(ott_id_list) == 1
    ott_id = ott_id_list[0]
    assert ott_id is not None
    output = OT.synth_node_info(ott_id=ott_id, include_lineage=args.include_lineage)

print(json.dumps(output.response_dict, indent=2, sort_keys=True))
