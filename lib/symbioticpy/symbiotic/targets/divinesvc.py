from .. benchexec.tools.divine4 import Tool as DivineTool
from . tool import SymbioticBaseTool

class SymbioticTool(DivineTool, SymbioticBaseTool):
    """
    DIVINE integrated into Symbiotic
    """

    REQUIRED_PATHS = DivineTool.REQUIRED_PATHS

    def __init__(self, opts):
        SymbioticBaseTool.__init__(self, opts)
        self._memsafety = self._options.property.memsafety()

    def llvm_version(self):
        return '7.0.1'

    def set_environment(self, env, opts):
        """
        Set environment for the tool
        """
        if opts.devel_mode:
            env.prepend('PATH', '{0}/divine'.\
                        format(env.symbiotic_dir))
        opts.is32bit = False
        opts.generate_ll = True

    def cc(self):
        # use divine cc to use DiOS' headers
        return ['divine', 'cc', '-C,-Os', '-C,-fgnu89-inline',
                '-C,-Wno-unused-parameter', '-C,-Wno-unknown-attributes',
                '-C,-Wno-unused-label', '-C,-Wno-unknown-pragmas',
                '-C,-Wno-unused-command-line-argument', '-c']

    def actions_before_slicing(self, symbiotic):
        symbiotic.link_undefined(['__VERIFIER_atomic_begin',
                                  '__VERIFIER_atomic_end'])

   # not needed anymore?
   #def actions_before_verification(self, symbiotic):
   #    # link the DiOS environment
   #    newfile = symbiotic.curfile[:-3] + '-cc' + symbiotic.curfile[-3:]
   #    symbiotic.command(['divine', 'cc', symbiotic.curfile, '-o', newfile])
   #    symbiotic.curfile = newfile

    def cmdline(self, executable, options, tasks, propertyfile=None, rlimits={}):
        return DivineTool.cmdline(self, executable, options, tasks, propertyfile, rlimits)

