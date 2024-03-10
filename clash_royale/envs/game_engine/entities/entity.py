"""
Base entity components    
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from clash_royale.envs.game_engine.struct import Stats

if TYPE_CHECKING:
    from clash_royale.envs.game_engine.arena import Arena


class Entity:
    """
    Entity - a generic entity class.

    This class represents a basic entity.
    And 'entity' is something is present in the arena.
    Entities are expected to handle and define the way they are rendered
    and how they process logic, whatever that looks like.
    It is important to note that entities are not required to do anything!
    It's valid for them to simply not display or think,
    but most entities will do both.

    Entities also contain a structure that describes the entity stats.
    Entities should configure this structure to match the entity they are implementing. 

    Entities also have a state, which describes how this entity is being used.
    This state is NOT related to gameplay!

    An entity has these states:

                      +<------------------------------<+                                 
    Created -> Loaded +> Started -> Running -> Stopped +> Unloaded

    * Created - Entity is instantiated
    * Loaded - Entity is loaded into a collection, relevant load code is ran
    * Started - Entity is started, relevant start code is ran 
    * Running - Entity is running and working in some way
    * Stopped - Entity is stopped, relevant stop code is ran and entity is no longer working with data
    * Unloaded - Entity is unloaded, relevant unload code is ran
    """

    CREATED: int = 0
    LOADED: int = 1
    STARTED: int = 2
    STOPPED: int = 3
    UNLOADED: int = 4

    def __init__(self) -> None:

        self.state: int = Entity.CREATED  # Current entity state

        self.x: int = 0  # X Position
        self.y: int  = 0  # Y Position

        self.stats: Stats = Stats()  # Use default stats unless otherwise stated
        self.collection: Arena  # EntityCollection we are apart of

    @property
    def running(self) -> bool:
        """
        Determines if this entity is running.

        We simply check the state to see if we are started.

        :return: True if running, False if not
        :rtype: bool
        """

        return self.state == Entity.STARTED

    @property
    def arena(self) -> EntityCollection:
        """
        Alias for 'collection'

        :return: Collection we are apart of
        :rtype: EntityCollection
        """

        return self.collection

    def load(self):
        """
        Method called when this entity is loaded.

        This method is invoked when the entity is loaded into a high level component.
        THIS DOES NOT MEAN THE entity SHOULD GET READY FOR USE!
        That is the job of the start() method.
        Just because a entity is loaded does not mean that it will be used.

        It is recommended to put basic startup code here,
        or define some parameters that change at load time.
        You should NOT start any major components in use
        until the start() method is called!
        """

        self.state = Entity.LOADED

    def unload(self):
        """
        Method called when this entity is unloaded.

        This method is invoked when the entity is unloaded from a high level component.
        When this method is called,
        it is reasonable to assume that this entity is not going to be used again.
        entitys can use this a a sign that their work is done.

        It is recommended to make any final, permanent changes once this method is called.
        """

        self.state = Entity.UNLOADED

    def start(self):
        """
        Method called when this entity is started.

        This method is usually invoked by a high level component,
        but this can defiantly be invoked by a user,
        or even this entity itself when used discretely!

        Developers can really put anything they want in here,
        but it is recommended to start or invoke any components 
        that are necessary for this entity's operation,
        as it is very likely that this entity will start working soon!
        """

        self.state = Entity.STARTED

    def stop(self):
        """
        Method called when this entity is stopped.

        This method, like start(), is usually invoked by a high level component,
        but this can definitely be invoked by a user,
        or even this entity itself when used discretely!

        Developers can really put anything they want in here,
        but it is recommended to stop all components in use by this entity,
        as it will stop working soon.

        Do not do anything too permanent!
        This entity may be started again at a later date,
        in the case of a entity restart operation.
        Again, don't do anything crazy permanent,
        just stop all components, ideally in a way that can be started again.
        """

        self.state = Entity.STOPPED

    def render(self):
        """
        Asks this entity to render itself!

        How the entity does this can vary
        (and it may even be completely generalized),
        but any render based code will be placed here.

        TODO: We need to figure out what component entities will render to
        """

        pass

    def simulate(self):
        """
        Preforms entity simulation for this frame.

        This method is where all the simulation will occur.
        In most cases, this can be implemented via higher level components,
        and should be if your entity is 'trivial'
        TODO: Define terminology for 'trivial'

        Before each frame is generated,
        each entity on the board will be asked to simulate themselves.
        These operations can be anything,
        but they generally fall under these tasks:

        - Attack Determination - Are there any viable targets?
        - Attack Strategy - How do we attack any other entities?
        - Movement Strategy - How does this entity move?

        Of course, some entities can have more complicated logic
        but for the most part these three things are what the entity preforms.
        """

        pass


class EntityCollection(object):
    """
    EntityCollection - Class all entity collections MUST inherit!

    An EntityCollection is a component that manages multiple entities,
    The main goal of this component is to provide state management
    and storage for many entities.

    We keep the list of entity's in a simple list,
    for the sake of simplicity.
    TODO: Maybe we could implement a better data structure here

    It can be safely assumed that all methods defined here WILL
    be present in the final class that inherits us.
    """

    def __init__(self) -> None:

        # entity storage component
        self.entities = []

        self.running = False  # Value determining if we are running
        self.num_loaded = 0  # Number of entity's currently loaded
        self.max_loaded = 0  # Max number of entity's loaded

    def load_entity(self, entity: Entity) -> Entity:
        """
        Adds the given entity to the collection.

        We ensure that the 'load' method of the entity is called,
        and that no exceptions are encountered.
        If we do encounter an exception,
        then we will not load this entity!

        We also return the instance of the entity we loaded.

        :param entity: Entity to add
        :type entity: Entity
        :return: entity we loaded
        :rtype: Entity
        """

        # We passed the check, let's run the load method:

        try:

            entity.load()

        except Exception as e:

            # Load error occurred! Raise an exception!

            raise Exception("entity load() method failed! Not loading: {}".format(entity), e)

        # Add the entity to our collection:

        self._load_entity(entity)

        # Finally, return the entity:

        return entity

    def unload_entity(self, entity: Entity) -> Entity:
        """
        Removes the given entity from the collection.

        We ensure that the stop() and unload() methods are called as appropriate.
        if we do encounter an exception,
        then the entity will be forcefully unloaded,
        and no further methods(if any) will be called.

        We first call the stop() method if the entity is running,
        and then finally the unload() method.
        After these methods do their work
        (Or if an exception is encountered),
        then we unload the entity from the collection.

        We also return a copy of the entity we unloaded.

        :param entity: entity to unload
        :type entity: Entity
        :return: entity we unloaded
        :rtype: Entity
        """

        # Stop the entity if necessary:

        if entity.running:

            # Stop the entity, call the stop() method:

            entity.stop()

        # Now, run the unload method:

        try:

            entity.unload()

        except Exception as e:

            # Raise an exception of our own:

            raise Exception("entity failed to unload! Unloading: {}".format(entity), e)

        # Unload the entity:

        self._unload_entity(entity)

        # Return the entity:

        return entity

    def stop_entity(self, entity: Entity) -> Entity:
        """
        Stops the given entity.

        This is done by calling the entity's stop() method.
        We also return a copy of the entity we worked with.

        :param entity: entity to stop
        :type entity: Entity
        :return: entity we stopped
        :rtype: Entity
        :raise: entityStopException: If the entity stop() method fails
        """

        # Call the stop method:

        try:
        
            entity.stop()

        except Exception as e:

            # Raise an exception:

            self._unload_entity(entity)

            raise Exception("entity stop() method failed! Unloading: {}".format(entity), e)

        # Return the entity:

        return entity

    def start_entity(self, entity: Entity) -> Entity:
        """
        Starts the given entity.

        This is done by calling the start() method of the entity.
        We also return a copy of the entity we worked with.

        If this entity fails to start,
        then it will automatically removed!

        :param entity: entity to start
        :type entity: Entity
        :return: entity we started
        :rtype: Entity
        """

        # Call the start method:

        try:

            entity.start()

        except Exception as e:

            # entity failed to start! Unload it...

            self._unload_entity(entity)

            # Raise an exception:

            raise Exception("entity start() method failed! Unloading: {}".format(entity), e)

        # Return the entity:

        return entity

    def restart_entity(self, entity: Entity) -> Entity:
        """
        Restarts the given entity.

        This is done by calling the start() and stop()
        methods of the entity in question.
        The entity MUST be in a running position to start!
        We also return the entity we restarted.

        If the entity fails to start or stop,
        then the entity will be forcefully unloaded!

        :param entity: entity to restart
        :type entity: Baseentity
        :return: The entity we restarted
        :rtype: Baseentity
        """

        # Stop the entity

        self.stop_entity(entity)

        # Start the entity:

        self.start_entity(entity)

        # Return the entity in question:

        return entity

    def start(self):
        """
        Method used to start this entityCollection.

        We set our running status and start all loaded entitys.
        """

        # Set our running status:

        self.running = True

        # Start all connected entity's:

        for mod in self.entitys:

            # Determine if this entity needs starting:

            if not mod.running:

                # Start the entity:

                self.start_entity(mod)

    def stop(self):
        """
        Method used to stop this entityCollection.

        We set our running status,
        and stop all started entitys.

        Sub-classes should put stop code here to end their relevant components.
        """

        # Set our running status:

        self.running = False

        for mod in self.entitys:

            # Determine if this entity needs stopping:

            if mod.running:

                # Stop the entity:

                self.stop_entity(mod)

        return

    def _load_entity(self, mod: Entity):
        """
        Adds the entity to our collection. 

        This low-level method is not intended to
        be worked with by end users!

        :param mod: entity to add
        :type mod: Baseentity
        """

        # Create the data to be stored:

        temp = (mod,)

        # Add the entity to the collection:

        self.entitys = self.entitys + temp

        # Update our stats:

        self.max_loaded += 1
        self.num_loaded += 1

        # Attach the collection to the entity:

        mod.collection = self

    def _unload_entity(self, mod: Entity):
        """
        Low-level method for unloading entitys from the list.

        We do not call any methods or work with the entity in any way
        other than removing it from the data structure.

        :param mod: The entity in question to remove
        :type mod: Baseentity
        :param key: Key of the entity to remove
        :type key: str
        """

        # Convert the tuple into a list:

        temp = list(self.entitys)

        # Remove the offending entity:

        temp.remove(mod)

        # Set our list:

        self.entitys = tuple(temp)

        # Update our stats:

        self.num_loaded -= 1
