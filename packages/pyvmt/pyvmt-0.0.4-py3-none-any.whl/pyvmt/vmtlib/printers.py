#
#    Copyright 2022 Embedded Systems Unit, Fondazione Bruno Kessler
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#
'''
    Printers for VMT-LIB which include supported LTL operators
'''

from pysmt.smtlib.printers import SmtPrinter, SmtDagPrinter

class VmtPrinter(SmtPrinter):
    '''
        Printer which uses a tree representation of the formula
    '''
    #pylint: disable=missing-function-docstring

    def walk_ltl_g(self, formula):
        return self.walk_nary(formula, 'ltl.G')

    def walk_ltl_f(self, formula):
        return self.walk_nary(formula, 'ltl.F')

    def walk_ltl_u(self, formula):
        return self.walk_nary(formula, 'ltl.U')

    def walk_ltl_x(self, formula):
        return self.walk_nary(formula, 'ltl.X')

    def walk_ltl_r(self, formula):
        raise NotImplementedError

    def walk_next(self, formula):
        raise NotImplementedError

class VmtDagPrinter(SmtDagPrinter):
    '''
        Printer which uses a dag representation of the formula
    '''
    #pylint: disable=missing-function-docstring

    def walk_ltl_g(self, formula, args):
        return self.walk_nary(formula, args, 'ltl.G')

    def walk_ltl_f(self, formula, args):
        return self.walk_nary(formula, args, 'ltl.F')

    def walk_ltl_u(self, formula, args):
        return self.walk_nary(formula, args, 'ltl.U')

    def walk_ltl_x(self, formula, args):
        return self.walk_nary(formula, args, 'ltl.X')

    def walk_ltl_r(self, formula, args):
        raise NotImplementedError

    def walk_next(self, formula, args):
        raise NotImplementedError
