# Exploration

## Overview

This program provides data types for representing the exploration of
spaces that can defined (or abstracted) in terms of discrete decisions,
such as videogame levels with multiple rooms and also other things like
conversation trees or a city block grid.

It represents a `Map` as a multi-di-graph, indicating the connection(s)
between decisions, which can include information about prerequisites for
transitions as well as effects a transition might have on the world.
There is also a convention for representing unexplored regions using
specially-named nodes of the graph. An `Exploration` is a sequence of
`Map`s, along with a sequence of decisions indicating where the explorer
was at each step, a sequence of transitions indicating which transition
was taken at each step, and a sequence of states indicating extra state
at each step. These representations were developed with Metroidvania
games in mind.

Core capabilities include:

- Reasoning about reachability modulo transition requirements in terms of
  powers that must be possessed and/or tokens that must be spent for a
  transition. TODO
- The ability to represent fairly sophisticated game logic in the `Map`,
  and even construct playable maps. Game logic that can't be captured
  this way can still be represented through making custom changes to maps
  between exploration steps. TODO
- Creating maps and explorations from various text formats, including
  exploration journal formats. TODO

## Installing

Just run `pip install exploration`. The `egtool` script should be
installed along with the module.

## Usage

TODO

## Plans

TODO

## Changelog

TODO
