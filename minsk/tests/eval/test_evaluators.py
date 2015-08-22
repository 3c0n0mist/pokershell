import testtools

import minsk.model as model
import minsk.eval.evaluators
import minsk.eval.context as context


def parse_combo(line):
    cards_str = line.split()
    return [model.Card.parse(card) for card in cards_str]


def create_context(cards_str):
    parsed = parse_combo(cards_str)
    return context.EvalContext(*parsed)


class TestFourEvaluator(testtools.TestCase):
    def setUp(self):
        super().setUp()
        self.evaluator = minsk.eval.evaluators.FourEvaluator()

    def test_eval(self):
        combo = parse_combo('Js Jc Jh 2c 3c')
        outs = self.evaluator.get_outs(*combo)
        self.assertEqual({model.Card.parse('Jd')}, outs)

    def test_find(self):
        result = self.evaluator.find(create_context('Js Jc 2h Jh 2c 3c Jd'))
        self.assertEqual((model.Rank.JACK,), result)


class TestThreeEvaluator(testtools.TestCase):
    def setUp(self):
        super().setUp()
        self.evaluator = minsk.eval.evaluators.ThreeEvaluator()

    def test_find(self):
        result = self.evaluator.find(create_context('2h 2c 2d 5h Jh Js Jc'))
        self.assertEqual((model.Rank.JACK,), result)


class TestOnePairEvaluator(testtools.TestCase):
    def setUp(self):
        super().setUp()
        self.evaluator = minsk.eval.evaluators.OnePairEvaluator()

    def test_find(self):
        result = self.evaluator.find(create_context('2h 2c 5h Jh qs Jc'))
        self.assertEqual((model.Rank.JACK,), result)

    def test_find_better(self):
        context = create_context('2h 2c 2d 5h Jh qs Jc')
        self.assertRaises(ValueError, self.evaluator.find, context)


class TestHighCardEvaluator(testtools.TestCase):
    def setUp(self):
        super().setUp()
        self.evaluator = minsk.eval.evaluators.HighCardEvaluator()

    def test_find(self):
        result = self.evaluator.find(create_context('2h  5h Jh qs'))
        self.assertEqual((model.Rank.QUEEN,), result)


class TestFullHouseEvaluator(testtools.TestCase):
    def setUp(self):
        super().setUp()
        self.evaluator = minsk.eval.evaluators.FullHouseEvaluator()

    def test_find_32(self):
        result = self.evaluator.find(create_context('2h 2c 2d 5h Jh Jc'))
        self.assertEqual((model.Rank.DEUCE, model.Rank.JACK), result)

    def test_find_33(self):
        result = self.evaluator.find(create_context('2h 2c 2d 5h Jh Jc Jd'))
        self.assertEqual((model.Rank.JACK, model.Rank.DEUCE), result)


class TestTwoPairsEvaluator(testtools.TestCase):
    def setUp(self):
        super().setUp()
        self.evaluator = minsk.eval.evaluators.TwoPairsEvaluator()

    def test_find(self):
        result = self.evaluator.find(create_context('2h 2c 5h Jh Jc'))
        self.assertEqual((model.Rank.JACK, model.Rank.DEUCE, model.Rank.FIVE), result)


class TestFlushEvaluator(testtools.TestCase):
    def setUp(self):
        super().setUp()
        self.evaluator = minsk.eval.evaluators.FlushEvaluator()

    def test_find6(self):
        result = self.evaluator.find(create_context('Js Jc 5c Jh 2c 3c Jc qc'))
        self.assertEqual([model.Rank.QUEEN, model.Rank.JACK, model.Rank.FIVE],
                         result[0:3])

    def test_find5(self):
        result = self.evaluator.find(create_context('Js 9c 5c Jh 2c 3c tc'))
        self.assertEqual([model.Rank.TEN, model.Rank.NINE, model.Rank.FIVE], result[0:3])

    def test_find_none(self):
        result = self.evaluator.find(create_context('Js 9s 5c Jh 2c 3h tc'))
        self.assertIsNone(result)


class TestStraightEvaluator(testtools.TestCase):
    def setUp(self):
        super().setUp()
        self.evaluator = minsk.eval.evaluators.StraightEvaluator()

    def test_find_best(self):
        result = self.evaluator.find(create_context('Js qc tc 9h 8c 7c Jc qc'))
        self.assertEqual([model.Rank.QUEEN], result)

    def test_find(self):
        result = self.evaluator.find(create_context('3s 5c 4c 6h 6d 7c Jc qc'))
        self.assertEqual([model.Rank.SEVEN], result)

    def test_find_ace_down(self):
        result = self.evaluator.find(create_context('3s 5c 4c 2h Ah 7c Jc qc'))
        self.assertEqual([model.Rank.FIVE], result)

    def test_find_ace_up(self):
        result = self.evaluator.find(create_context('Js Kc Tc Jh 2c Ah Jc qc'))
        self.assertEqual([model.Rank.ACE], result)


class TestStraightFlushEvaluator(testtools.TestCase):
    def setUp(self):
        super().setUp()
        self.evaluator = minsk.eval.evaluators.StraightFlushEvaluator()

    def test_find(self):
        result = self.evaluator.find(create_context('Jh qh th 9h 8h 7h Jc qc'))
        self.assertEqual([model.Rank.QUEEN], result)

    def test_find_ace_down(self):
        result = self.evaluator.find(create_context('3h 5h 4h 2h Ah 7c Jc qc'))
        self.assertEqual([model.Rank.FIVE], result)

    def test_find_ace_up(self):
        result = self.evaluator.find(create_context('Js Kc Tc Jh 2c Ac Jc qc'))
        self.assertEqual([model.Rank.ACE], result)
