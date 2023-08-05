import logging
import os

from typing import Dict, List, Tuple
from autobridge.Floorplan.Partition import partition
from autobridge.Floorplan.IterativeBipartion import iterative_bipartition
from autobridge.Floorplan.Utilities import (
  print_pre_assignment,
  print_vertex_areas,
  get_eight_way_partition_slots,
  get_four_way_partition_slots,
)
from autobridge.Opt.DataflowGraph import Vertex, DataflowGraph
from autobridge.Opt.Slot import Slot
from autobridge.Opt.SlotManager import SlotManager, Dir

_logger = logging.getLogger('autobridge')


def get_floorplan(
  graph: DataflowGraph,
  slot_manager: SlotManager,
  grouping_constraints_in_str: List[List[str]],
  pre_assignments_in_str: Dict[str, str],
  floorplan_strategy: str = 'HALF_SLR_LEVEL_FLOORPLANNING',
  threshold_for_iterative: int = 400,
  floorplan_opt_priority: str = 'AREA_PRIORITIZED',
) -> Tuple[Dict[Vertex, Slot], List[Slot]]:
  """
  main entrance of the floorplan part
  return (1) mapping from vertex to slot
  (2) a list of all potential slots
  Note that an empty slot will not be in (1), but will occur in (2)
  """
  # get initial v2s
  init_slot = slot_manager.getInitialSlot()
  init_v2s = {v : init_slot for v in graph.getAllVertices()}

  # get grouping constraints of Vertex
  grouping_constraints: List[List[Vertex]] = [
    [graph.getVertex(v_name) for v_name in v_name_group]
      for v_name_group in grouping_constraints_in_str
  ]

  _logger.info(f'The following modules are grouped to the same location:')
  for grouping in grouping_constraints_in_str:
    _logger.info('    ' + ', '.join(grouping))

  # get pre_assignment in Vertex
  pre_assignments = { graph.getVertex(v_name) : slot_manager.createSlot(pblock)
    for v_name, pblock in pre_assignments_in_str.items()
  }

  print_pre_assignment(pre_assignments)

  print_vertex_areas(init_v2s.keys())

  # choose floorplan method
  num_vertices = len(graph.getAllVertices())
  v2s: Dict[Vertex, Slot] = {}

  # if user specifies floorplan methods
  if floorplan_strategy == 'SLR_LEVEL_FLOORPLANNING':
    _logger.info(f'user specifies to floorplan into SLR-level slots')
    v2s = partition(
      init_v2s, slot_manager, grouping_constraints, pre_assignments, partition_method='FOUR_WAY_PARTITION', priority=floorplan_opt_priority
    )

    if v2s:
      return v2s, get_four_way_partition_slots(slot_manager)
    else:
      return None

  elif floorplan_strategy == 'QUICK_FLOORPLANNING':
    _logger.info(f'user specifies to prioritize speed')
    v2s = iterative_bipartition(init_v2s, slot_manager, grouping_constraints, pre_assignments)
    if v2s:
      return v2s
    else:
      return None

  else:
    if floorplan_strategy is not 'HALF_SLR_LEVEL_FLOORPLANNING':
      raise NotImplementedError('unrecognized floorplan strategy %s', floorplan_strategy)

  # empirically select the floorplan method
  if num_vertices < threshold_for_iterative:
    _logger.info(f'There are {num_vertices} vertices in the design, use eight way partition')

    if num_vertices > 100:
      _logger.warning('Over 100 vertices. May have a long solving time. Reduce threshold_for_iterative to skip to iterative bi-partitioning.')

    v2s = partition(
      init_v2s, slot_manager, grouping_constraints, pre_assignments, partition_method='EIGHT_WAY_PARTITION', priority=floorplan_opt_priority
    )
    if v2s:
      return v2s, get_eight_way_partition_slots(slot_manager)
    else:
      _logger.warning(f'Please check if any function in the design is too large')

  else:
    _logger.info(f'Use four-way partition because eight-way partition failed or there are too many vertices ({num_vertices})')
    v2s = partition(
      init_v2s, slot_manager, grouping_constraints, pre_assignments, partition_method='FOUR_WAY_PARTITION', priority=floorplan_opt_priority
    )
    if v2s:
      return v2s, get_four_way_partition_slots(slot_manager)

  _logger.error(f'AutoBridge fails to partition the design at the SLR level. Either the design is too large, or the functions/modules are too large.')
  return None, None
