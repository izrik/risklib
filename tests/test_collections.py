from unittest import TestCase

from riskcli import Territory, Player, Continent


class PlayerTerritoriesTest(TestCase):
    def test_add_territory_to_player_also_sets_owner(self):
        # given
        t = Territory('t')
        p = Player('p', 'red')
        # precondition
        self.assertIsNone(t.owner)
        self.assertEqual(set(), set(p.territories))
        # when
        p.territories.add(t)
        # then
        self.assertIs(p, t.owner)
        self.assertEqual(1, len(p.territories))
        self.assertEqual({t}, set(p.territories))

    def test_set_owner_also_adds_territory_to_player(self):
        # given
        t = Territory('t')
        p = Player('p', 'red')
        # precondition
        self.assertIsNone(t.owner)
        self.assertEqual(set(), set(p.territories))
        # when
        t.owner = p
        # then
        self.assertIs(p, t.owner)
        self.assertEqual(1, len(p.territories))
        self.assertEqual({t}, set(p.territories))

    def test_set_owner_to_none_also_removes_territory_from_player(self):
        # given
        t = Territory('t')
        p = Player('p', 'red')
        t.owner = p
        # precondition
        self.assertIs(p, t.owner)
        self.assertEqual({t}, set(p.territories))
        # when
        t.owner = None
        # then
        self.assertIsNone(t.owner)
        self.assertEqual(0, len(p.territories))
        self.assertEqual(set(), set(p.territories))

    def test_remove_territory_from_player_also_sets_owner_to_none(self):
        # given
        t = Territory('t')
        p = Player('p', 'red')
        t.owner = p
        # precondition
        self.assertIs(p, t.owner)
        self.assertEqual({t}, set(p.territories))
        # when
        p.territories.remove(t)
        # then
        self.assertIsNone(t.owner)
        self.assertEqual(0, len(p.territories))
        self.assertEqual(set(), set(p.territories))

    def test_change_owner_also_updates_territories_for_both_players(self):
        # given
        t = Territory('t')
        p1 = Player('p1', 'red')
        p2 = Player('p2', 'blue')
        t.owner = p1
        # precondition
        self.assertIs(p1, t.owner)
        self.assertEqual({t}, set(p1.territories))
        self.assertEqual(set(), set(p2.territories))
        # when
        t.owner = p2
        # then
        self.assertIs(p2, t.owner)
        self.assertEqual(set(), set(p1.territories))
        self.assertEqual({t}, set(p2.territories))

    def test_add_territory_to_new_owner_also_removes_from_old_owner(self):
        # given
        t = Territory('t')
        p1 = Player('p1', 'red')
        p2 = Player('p2', 'blue')
        t.owner = p1
        # precondition
        self.assertIs(p1, t.owner)
        self.assertEqual({t}, set(p1.territories))
        self.assertEqual(set(), set(p2.territories))
        # when
        p2.territories.add(t)
        # then
        self.assertIs(p2, t.owner)
        self.assertEqual(set(), set(p1.territories))
        self.assertEqual({t}, set(p2.territories))


class TerritoryNeighborsTest(TestCase):
    def test_add_neighbor_to_territory_also_adds_territory_to_neighbor(self):
        # given
        t1 = Territory('t1')
        t2 = Territory('t2')
        # precondition
        self.assertEqual(set(), set(t1.neighbors))
        self.assertEqual(set(), set(t2.neighbors))
        # when
        t1.neighbors.add(t2)
        # then
        self.assertEqual({t2}, set(t1.neighbors))
        self.assertEqual({t1}, set(t2.neighbors))

    def test_remove_from_one_also_removes_from_the_other(self):
        # given
        t1 = Territory('t1')
        t2 = Territory('t2')
        t1.neighbors.add(t2)
        # precondition
        self.assertEqual({t2}, set(t1.neighbors))
        self.assertEqual({t1}, set(t2.neighbors))
        # when
        t1.neighbors.remove(t2)
        # then
        self.assertEqual(set(), set(t1.neighbors))
        self.assertEqual(set(), set(t2.neighbors))


class ContinentTerritoriesTest(TestCase):
    def test_add_territory_to_continent_also_sets_continent(self):
        # given
        t = Territory('t')
        c = Continent('c')
        # precondition
        self.assertIsNone(t.continent)
        self.assertEqual(set(), set(c.territories))
        # when
        c.territories.add(t)
        # then
        self.assertIs(c, t.continent)
        self.assertEqual(1, len(c.territories))
        self.assertEqual({t}, set(c.territories))

    def test_set_continent_also_adds_territory_to_continent(self):
        # given
        t = Territory('t')
        c = Continent('c')
        # precondition
        self.assertIsNone(t.continent)
        self.assertEqual(set(), set(c.territories))
        # when
        t.continent = c
        # then
        self.assertIs(c, t.continent)
        self.assertEqual(1, len(c.territories))
        self.assertEqual({t}, set(c.territories))

    def test_set_continent_to_none_also_removes_territory_from_continent(self):
        # given
        t = Territory('t')
        c = Continent('c')
        t.continent = c
        # precondition
        self.assertIs(c, t.continent)
        self.assertEqual({t}, set(c.territories))
        # when
        t.continent = None
        # then
        self.assertIsNone(t.continent)
        self.assertEqual(0, len(c.territories))
        self.assertEqual(set(), set(c.territories))

    def test_remove_territory_from_continent_also_sets_continent_to_none(self):
        # given
        t = Territory('t')
        c = Continent('c')
        t.continent = c
        # precondition
        self.assertIs(c, t.continent)
        self.assertEqual({t}, set(c.territories))
        # when
        c.territories.remove(t)
        # then
        self.assertIsNone(t.continent)
        self.assertEqual(0, len(c.territories))
        self.assertEqual(set(), set(c.territories))

    def test_change_continent_also_updates_territories_for_both(self):
        # given
        t = Territory('t')
        c1 = Continent('c1', 'red')
        c2 = Continent('c2', 'blue')
        t.continent = c1
        # precondition
        self.assertIs(c1, t.continent)
        self.assertEqual({t}, set(c1.territories))
        self.assertEqual(set(), set(c2.territories))
        # when
        t.continent = c2
        # then
        self.assertIs(c2, t.continent)
        self.assertEqual(set(), set(c1.territories))
        self.assertEqual({t}, set(c2.territories))

    def test_add_territory_to_new_continent_also_removes_from_old(self):
        # given
        t = Territory('t')
        c1 = Continent('c1', 'red')
        c2 = Continent('c2', 'blue')
        t.continent = c1
        # precondition
        self.assertIs(c1, t.continent)
        self.assertEqual({t}, set(c1.territories))
        self.assertEqual(set(), set(c2.territories))
        # when
        c2.territories.add(t)
        # then
        self.assertIs(c2, t.continent)
        self.assertEqual(set(), set(c1.territories))
        self.assertEqual({t}, set(c2.territories))
