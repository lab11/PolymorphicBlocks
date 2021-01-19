package edg.util

import scala.collection.mutable


/** A dependency graph data structure, containing Key -> Key directed edges can be added, and Key -> Value mappings.
  * A node is "ready" when all its input edges have values.
  * Must be acyclic.
  * Tracks the frontier, so getReady() is fast.
  */
class DependencyGraph[KeyType, ValueType] {
  private val values = mutable.HashMap[KeyType, ValueType]()
  private val inverseDeps = mutable.HashMap[KeyType, mutable.Set[KeyType]]()

  private val deps = mutable.HashMap[KeyType, mutable.Set[KeyType]]()  // cache structure tracking undefined deps
  // Key should be retained (even if value-set is empty) once addNode called
  private val ready = mutable.Set[KeyType]()

  // Adds a node in the graph. May only be called once per node.
  def addNode(node: KeyType, dependencies: Seq[KeyType]): Unit = {
    require(!deps.isDefinedAt(node))
    val remainingDeps = mutable.Set(dependencies: _*) -- values.keySet

    deps.put(node, remainingDeps)
    for (dependency <- remainingDeps) {
      inverseDeps.getOrElseUpdate(dependency, mutable.Set()) += node
    }

    if (remainingDeps.isEmpty) {
      ready += node
    }
  }

  // Sets the value of a node. May not overwrite values.
  def setValue(node: KeyType, value: ValueType): Unit = {
    require(!values.isDefinedAt(node), s"redefinition of $node")
    values.put(node, value)
    if (ready.contains(node)) {
      ready -= node
    }

    // See if the update caused anything else to be ready
    for (inverseDep <- inverseDeps.getOrElse(node, mutable.Set())) {
      val remainingDeps = deps(inverseDep) -= node
      if (remainingDeps.isEmpty) {
        ready += inverseDep
      }
    }
  }

  def getValue(node: KeyType): Option[ValueType] = {
    values.get(node)
  }

  // Returns all the KeyTypes that don't have values and have satisfied dependencies.
  def getReady(): Set[KeyType] = {
    ready.toSet
  }
}

object DependencyGraph {
  def apply[KeyType, ValueType](): DependencyGraph[KeyType, ValueType] = new DependencyGraph[KeyType, ValueType]
}
