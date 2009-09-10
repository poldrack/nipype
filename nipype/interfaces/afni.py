"""Provide interface to AFNI commands."""
__docformat__ = 'restructuredtext'


from nipype.interfaces.base import Bunch, CommandLine
from nipype.utils.docparse import get_doc

class AFNICommand(CommandLine):
    @property
    def cmdline(self):
        """Generate the command line string from the list of arguments."""
        allargs = self._parseinputs()
        allargs.insert(0, self.cmd)
        return ' '.join(allargs)


class To3d(AFNICommand):
    """Create a 3D dataset from 2D image files using AFNI to3d command.

    For complete details, see the `to3d Documentation. 
    <http://afni.nimh.nih.gov/pub/dist/doc/program_help/to3d.html>`_

    To print out the command line help, use:
        To3d().inputs_help()

    Examples
    --------
    Basic usage examples.

    >>> to3d = afni.To3d(datatype="anat")
    >>> to3d.inputs.datum = 'float'
    >>> to3d.run()

    """

    @property
    def cmd(self):
        """Base command for To3d"""
        return 'to3d'

    def inputs_help(self):
        """Print command line documentation for to3d."""
        #print get_doc(self.cmd, self.opt_map)
        raise NotImplementedError

    def _populate_inputs(self):
        """Initialize the inputs attribute."""
        self.inputs = Bunch(datatype=None,
                            skip_outliers=None,
                            assume_dicom_mosaic=None,
                            datum=None,
                            time_dependencies=None,
                            session=None,
                            prefix=None,
                            infiles=None)

    def _parseinputs(self):
        """Parse valid input options for To3d command.

        Ignore options set to None.

        """

        out_inputs = []
        inputs = {}
        [inputs.update({k:v}) for k, v in self.inputs.iteritems() \
            if v is not None]

        if inputs.has_key('datatype'):
            val = inputs.pop('datatype')
            out_inputs.append('-%s' % val)
        if inputs.has_key('skip_outliers'):
            val = inputs.pop('skip_outliers')
            out_inputs.append('-skip_outliers')
        if inputs.has_key('assume_dicom_mosaic'):
            val = inputs.pop('assume_dicom_mosaic')
            out_inputs.append('-assume_dicom_mosaic')
        if inputs.has_key('datum'):
            val = inputs.pop('datum')
            out_inputs.append('-datum %s' % val)
        if inputs.has_key('time_dependencies'):
            val = inputs.pop('time_dependencies')
            inputssub = {}
            [inputssub.update({k:v}) for k, v in val.iteritems() \
                if v is not None]

            # -time:zt nz nt TR tpattern  OR  -time:tz nt nz TR tpattern
            # time : list
            #    zt nz nt TR tpattern
            #    tz nt nz TR tpattern
            # TODO: ABOVE DOC IS OLD

            # dict(slice_order='zt', nz=12, nt=150, TR=2000, tpattern='alt+z')
            _time_dep_doc = \
            """
            time_dependencies should be a dictionary with the follow keys 
            assigned:
            slice_order, nz, nt, TR, tpattern

            """

            try:
                slice_order = inputssub.pop('slice_order')
                out_inputs.append('-time:%s' % slice_order)
            except KeyError:
                raise KeyError('slice_order is required for time_dependencies')
            try:
                nz = inputssub.pop('nz')
            except KeyError:
                raise KeyError('nz required for time_dependencies')
            try:
                nt = inputssub.pop('nt')
            except KeyError:
                raise KeyError('nt required for time_dependencies')

            if slice_order == 'tz':
                out_inputs.append('%s' % str(nt))
                out_inputs.append('%s' % str(nz))
            else:
                out_inputs.append('%s' % str(nz))
                out_inputs.append('%s' % str(nt))

            try:
                valsub = inputssub.pop('TR')
                out_inputs.append('%s' % str(valsub))
            except KeyError:
                raise KeyError('TR required for time_dependencies')
            try:
                valsub = inputssub.pop('tpattern')
                out_inputs.append('%s' % valsub)
            except KeyError:
                raise KeyError('tpattern required for time_dependencies')

            if len(inputssub) > 0:
                msg = '%s: unsupported time_dependencies options: %s' % (
                    self.__class__.__name__, inputssub.keys())
                raise AttributeError(msg)

        if inputs.has_key('session'):
            val = inputs.pop('session')
            out_inputs.append('-session %s' % val)
        if inputs.has_key('prefix'):
            val = inputs.pop('prefix')
            out_inputs.append('-prefix %s' % val)
        if inputs.has_key('infiles'):
            val = inputs.pop('infiles')
            out_inputs.append('%s' % val)

        if len(inputs) > 0:
            msg = '%s: unsupported options: %s' % (
                self.__class__.__name__, inputs.keys())
            raise AttributeError(msg)

        return out_inputs


class Threedrefit(AFNICommand):
    """Fix errors in AFNI header resulting from using to3d command.

    For complete details, see the `3drefit Documentation. 
    <http://afni.nimh.nih.gov/pub/dist/doc/program_help/3drefit.html>`_
    """

    @property
    def cmd(self):
        """Base command for Threedrefit"""
        return '3drefit'

    def inputs_help(self):
        doc = """
          Optional Parameters
          -------------------
        """
        print doc

    def _populate_inputs(self):
        """Initialize the inputs attribute."""
        self.inputs = Bunch(deoblique=None,
                            xorigin=None,
                            yorigin=None,
                            zorigin=None,
                            infile=None)

    def _parseinputs(self):
        """Parse valid input options for Threedrefit command.

        Ignore options set to None.

        """

        out_inputs = []
        inputs = {}
        [inputs.update({k:v}) for k, v in self.inputs.iteritems() \
             if v is not None]

        if inputs.has_key('deoblique'):
            val = inputs.pop('deoblique')
            out_inputs.append('-deoblique')
        if inputs.has_key('xorigin'):
            val = inputs.pop('xorigin')
            out_inputs.append('-xorigin %s' % val)
        if inputs.has_key('yorigin'):
            val = inputs.pop('yorigin')
            out_inputs.append('-yorigin %s' % val)
        if inputs.has_key('zorigin'):
            val = inputs.pop('zorigin')
            out_inputs.append('-zorigin %s' % val)
        if inputs.has_key('infile'):
            val = inputs.pop('infile')
            out_inputs.append('%s' % val)

        if len(inputs) > 0:
            msg = '%s: unsupported options: %s' % (
                self.__class__.__name__, inputs.keys())
            raise AttributeError(msg)

        return out_inputs

    def run(self, infile=None, **inputs):
        """Execute the command.

        Parameters
        ----------
        infile : filename
            File whose header file will be updated by 3drefit
        
        Returns
        -------
        results : InterfaceResult
            A `InterfaceResult` object with a copy of self in `interface`

        """
        if infile:
            self.inputs.infile = infile
        if not self.inputs.infile:
            raise AttributeError('Threedrefit requires an infile.')
        self.inputs.update(**inputs)
        results = self._runner()
        # XXX implement aggregate_outputs
        return results
        

class Threedresample(AFNICommand):
    """Resample or reorient an image using AFNI 3dresample command.

    For complete details, see the `3dresample Documentation. 
    <http://afni.nimh.nih.gov/pub/dist/doc/program_help/3dresample.html>`_
    """

    @property
    def cmd(self):
        """Base command for Threedresample"""
        return '3dresample'

    def inputs_help(self):
        doc = """
          Optional Parameters
          -------------------
        """
        print doc

    def _populate_inputs(self):
        """Initialize the inputs attribute."""

        self.inputs = Bunch(rsmode=None,
                            orient=None,
                            gridfile=None,
                            outfile=None,
                            infile=None)

    def _parseinputs(self):
        """Parse valid input options for Threedresample command.

        Ignore options set to None.

        """

        out_inputs = []
        inputs = {}
        [inputs.update({k:v}) for k, v in self.inputs.iteritems() \
             if v is not None]

        if inputs.has_key('rsmode'):
            val = inputs.pop('rsmode')
            out_inputs.append('-rmode %s' % val)
        if inputs.has_key('orient'):
            val = inputs.pop('orient')
            out_inputs.append('-orient %s' % val)
        if inputs.has_key('gridfile'):
            val = inputs.pop('gridfile')
            out_inputs.append('-master %s' % val)
        if inputs.has_key('outfile'):
            val = inputs.pop('outfile')
            out_inputs.append('-prefix %s' % val)
        if inputs.has_key('infile'):
            val = inputs.pop('infile')
            out_inputs.append('-inset %s' % val)

        if len(inputs) > 0:
            msg = '%s: unsupported options: %s' % (
                self.__class__.__name__, inputs.keys())
            raise AttributeError(msg)

        return out_inputs

    def run(self, infile=None, outfile=None, **inputs):
        """Execute 3dresample.

        Parameters
        ----------
        infile : filename
            File that we be resampled
        outfile : filename
            Output file name or prefix for output file name.
        inputs : dict
            Dictionary of any additional flags to send to 3dresample

        Returns
        -------
        results : InterfaceResult
            A `InterfaceResult` object with a copy of self in `interface`

        """
        if infile:
            self.inputs.infile = infile
        if outfile:
            self.inputs.outfile = outfile
        if not self.inputs.infile or not self.inputs.outfile:
            msg = 'Threedresample requires an infile and an outfile.'
            raise AttributeError(msg)
        self.inputs.update(**inputs)
        results = self._runner()
        # XXX implement aggregate_outputs
        return results

        
class ThreedTstat(AFNICommand):
    """Compute voxel-wise statistices using AFNI 3dTstat command.

    For complete details, see the `3dTstat Documentation. 
    <http://afni.nimh.nih.gov/pub/dist/doc/program_help/3dTstat.html>`_
    """

    @property
    def cmd(self):
        """Base command for ThreedTstat"""
        return '3dTstat'

    def inputs_help(self):
        doc = """
          Optional Parameters
          -------------------
        """
        print doc

    def _populate_inputs(self):
        """Initialize the inputs attribute."""

        self.inputs = Bunch(outfile=None,
                            infile=None)

    def _parseinputs(self):
        """Parse valid input options for ThreedTstat command.

        Ignore options set to None.

        """

        out_inputs = []
        inputs = {}
        [inputs.update({k:v}) for k, v in self.inputs.iteritems() \
             if v is not None]

        if inputs.has_key('outfile'):
            val = inputs.pop('outfile')
            out_inputs.append('-prefix %s' % val)
        if inputs.has_key('infile'):
            val = inputs.pop('infile')
            out_inputs.append('%s' % val)

        if len(inputs) > 0:
            msg = '%s: unsupported options: %s' % (
                self.__class__.__name__, inputs.keys())
            raise AttributeError(msg)

        return out_inputs

    def run(self, infile=None, **inputs):
        """Execute 3dTstat

        Parameters
        ----------
        infile : filename
            File that we be resampled
        inputs : dict
            Dictionary of any additional flags to send to 3dresample

        Returns
        -------
        results : InterfaceResult
            A `InterfaceResult` object with a copy of self in `interface`

        """
        if infile:
            self.inputs.infile = infile
        if not self.inputs.infile:
            raise AttributeError('ThreedTstat requires an infile.')
        self.inputs.update(**inputs)
        results = self._runner()
        # XXX implement aggregate_outputs
        return results


class ThreedAutomask(AFNICommand):
    """
    For complete details, see the `to3d Documentation. 
    <http://afni.nimh.nih.gov/pub/dist/doc/program_help/3dAutomask.html>`_
    """

    @property
    def cmd(self):
        """Base command for ThreedAutomask"""
        return '3dAutomask'

    def inputs_help(self):
        doc = """
          Optional Parameters
          -------------------
        """
        print doc

    def _populate_inputs(self):
        """Initialize the inputs attribute."""

        self.inputs = Bunch(outfile=None,
                            infile=None)

    def _parseinputs(self):
        """Parse valid input options for ThreedAutomask command.

        Ignore options set to None.

        """

        out_inputs = []
        inputs = {}
        [inputs.update({k:v}) for k, v in self.inputs.iteritems() \
             if v is not None]

        if inputs.has_key('outfile'):
            val = inputs.pop('outfile')
            out_inputs.append('-prefix %s' % val)
        if inputs.has_key('infile'):
            val = inputs.pop('infile')
            out_inputs.append('%s' % val)

        if len(inputs) > 0:
            print '%s: unsupported options: %s' % (
                self.__class__.__name__, inputs.keys())

        return out_inputs


class Threedvolreg(AFNICommand):
    """
    For complete details, see the `to3d Documentation. 
    <http://afni.nimh.nih.gov/pub/dist/doc/program_help/3dvolreg.html>`_
    """

    @property
    def cmd(self):
        """Base command for Threedvolreg"""
        return '3dvolreg'

    def inputs_help(self):
        doc = """
          Optional Parameters
          -------------------
        """
        print doc

    def _populate_inputs(self):
        """Initialize the inputs attribute."""

        self.inputs = Bunch(
            verbose=None,
            copy_origin=None,
            time_shift=None,
            basefile=None,
            md1dfile=None,
            onedfile=None,
            outfile=None,
            infile=None)

    def _parseinputs(self):
        """Parse valid input options for Threedvolreg command.

        Ignore options set to None.

        """

        out_inputs = []
        inputs = {}
        [inputs.update({k:v}) for k, v in self.inputs.iteritems() \
             if v is not None]

        if inputs.has_key('verbose'):
            val = inputs.pop('verbose')
            out_inputs.append('-verbose')
        if inputs.has_key('copy_origin'):
            val = inputs.pop('copy_origin')
            out_inputs.append('-twodup')
        if inputs.has_key('time_shift'):
            val = inputs.pop('time_shift')
            out_inputs.append('-tshift %s' % str(val))
        if inputs.has_key('basefile'):
            val = inputs.pop('basefile')
            out_inputs.append('-base %s' % val)
        if inputs.has_key('md1dfile'):
            val = inputs.pop('md1dfile')
            out_inputs.append('-maxdisp1D %s' % val)
        if inputs.has_key('onedfile'):
            val = inputs.pop('onedfile')
            out_inputs.append('-1Dfile %s' % val)
        if inputs.has_key('outfile'):
            val = inputs.pop('outfile')
            out_inputs.append('-prefix %s' % val)
        if inputs.has_key('infile'):
            val = inputs.pop('infile')
            out_inputs.append('%s' % val)

        if len(inputs) > 0:
            print '%s: unsupported options: %s' % (
                self.__class__.__name__, inputs.keys())

        return out_inputs


class Threedmerge(AFNICommand):
    """
    For complete details, see the `to3d Documentation. 
    <http://afni.nimh.nih.gov/pub/dist/doc/program_help/3dmerge.html>`_
    """

    @property
    def cmd(self):
        """Base command for Threedmerge"""
        return '3dmerge'

    def inputs_help(self):
        doc = """
          Optional Parameters
          -------------------
        """
        print doc

    def _populate_inputs(self):
        """Initialize the inputs attribute."""

        self.inputs = Bunch(
            doall=None,
            gblur_fwhm=None,
            outfile=None,
            infile=None)

    def _parseinputs(self):
        """Parse valid input options for Threedmerge command.

        Ignore options set to None.

        """

        out_inputs = []
        inputs = {}
        [inputs.update({k:v}) for k, v in self.inputs.iteritems() \
             if v is not None]

        if inputs.has_key('doall'):
            val = inputs.pop('doall')
            out_inputs.append('-doall')
        if inputs.has_key('gblur_fwhm'):
            val = inputs.pop('gblur_fwhm')
            out_inputs.append('-1blur_fwhm %s' % str(val))
        if inputs.has_key('outfile'):
            val = inputs.pop('outfile')
            out_inputs.append('-prefix %s' % val)
        if inputs.has_key('infile'):
            val = inputs.pop('infile')
            out_inputs.append('%s' % val)

        if len(inputs) > 0:
            print '%s: unsupported options: %s' % (
                self.__class__.__name__, inputs.keys())

        return out_inputs


class ThreedZcutup(AFNICommand):
    """
    For complete details, see the `to3d Documentation. 
    <http://afni.nimh.nih.gov/pub/dist/doc/program_help/3dZcutup.html>`_
    """

    @property
    def cmd(self):
        """Base command for ThreedZcutup"""
        return '3dZcutup'

    def inputs_help(self):
        doc = """
          Optional Parameters
          -------------------
        """
        print doc

    def _populate_inputs(self):
        """Initialize the inputs attribute."""

        self.inputs = Bunch(
            keep=[],
            outfile=None,
            infile=None)

    def _parseinputs(self):
        """Parse valid input options for ThreedZcutup command.

        Ignore options set to None.

        """

        out_inputs = []
        inputs = {}
        [inputs.update({k:v}) for k, v in self.inputs.iteritems() \
             if v is not None]

        if inputs.has_key('keep'):
            val = inputs.pop('keep')
            inputssub = {}
            [inputssub.update({k:v}) for k, v in val.iteritems() \
                if v is not None]

            if inputssub.has_key('from'):
                valsub = inputssub.pop('from')
                out_inputs.append('-keep %s' % str(valsub))
            else:
                valsub=None
                print('Warning: value \'from\' required for keep')
            if inputssub.has_key('to'):
                valsub = inputssub.pop('to')
                out_inputs.append('%s' % str(valsub))
            else:
                valsub=None
                print('Warning: value \'to\' required for keep')
        if inputs.has_key('outfile'):
            val = inputs.pop('outfile')
            out_inputs.append('-prefix %s' % val)
        if inputs.has_key('infile'):
            val = inputs.pop('infile')
            out_inputs.append('%s' % val)

        if len(inputs) > 0:
            print '%s: unsupported options: %s' % (
                self.__class__.__name__, inputs.keys())

        return out_inputs


class ThreedSkullStrip(AFNICommand):
    """
    For complete details, see the `to3d Documentation. 
    <http://afni.nimh.nih.gov/pub/dist/doc/program_help/3dSkullStrip.html>`_
    """

    @property
    def cmd(self):
        """Base command for ThreedSkullStrip"""
        return '3dSkullStrip'

    def inputs_help(self):
        doc = """
          Optional Parameters
          -------------------
        """
        print doc

    def _populate_inputs(self):
        """Initialize the inputs attribute."""

        self.inputs = Bunch(outfile=None,
                            infile=None)

    def _parseinputs(self):
        """Parse valid input options for ThreedSkullStrip command.

        Ignore options set to None.

        """

        out_inputs = []
        inputs = {}
        [inputs.update({k:v}) for k, v in self.inputs.iteritems() \
             if v is not None]

        if inputs.has_key('outfile'):
            val = inputs.pop('outfile')
            out_inputs.append('-prefix %s' % val)
        if inputs.has_key('infile'):
            val = inputs.pop('infile')
            out_inputs.append('-input %s' % val)

        if len(inputs) > 0:
            print '%s: unsupported options: %s' % (
                self.__class__.__name__, inputs.keys())

        return out_inputs


class ThreedBrickStat(AFNICommand):
    """
    For complete details, see the `to3d Documentation. 
    <http://afni.nimh.nih.gov/pub/dist/doc/program_help/3dBrickStat.html>`_
    """

    @property
    def cmd(self):
        """Base command for ThreedBrickStat"""
        return '3dBrickStat'

    def inputs_help(self):
        doc = """
          Optional Parameters
          -------------------
        """
        print doc

    def _populate_inputs(self):
        """Initialize the inputs attribute."""

        self.inputs = Bunch(automask=None,
                            percentile=None,
                            infile=None)

    def _parseinputs(self):
        """Parse valid input options for ThreedBrickStat command.

        Ignore options set to None.

        """

        out_inputs = []
        inputs = {}
        [inputs.update({k:v}) for k, v in self.inputs.iteritems() \
             if v is not None]

        if inputs.has_key('automask'):
            val = inputs.pop('automask')
            out_inputs.append('-automask')
        if inputs.has_key('percentile'):
            val = inputs.pop('percentile')
            inputssub = {}
            [inputssub.update({k:v}) for k, v in val.iteritems() \
                if v is not None]

            if inputssub.has_key('p0'):
                valsub = inputssub.pop('p0')
                out_inputs.append('-percentile %s' % str(valsub))
            else:
                valsub=None
                print('Warning: value \'p0\' required for percentile')
            if inputssub.has_key('pstep'):
                valsub = inputssub.pop('pstep')
                out_inputs.append('%s' % str(valsub))
            else:
                valsub=None
                print('Warning: value \'pstep\' required for percentile')
            if inputssub.has_key('p1'):
                valsub = inputssub.pop('p1')
                out_inputs.append('%s' % str(valsub))
            else:
                valsub=None
                print('Warning: value \'p1\' required for percentile')

        if inputs.has_key('infile'):
            val = inputs.pop('infile')
            out_inputs.append('%s' % val)

        if len(inputs) > 0:
            print '%s: unsupported options: %s' % (
                self.__class__.__name__, inputs.keys())

        return out_inputs


class Threedcalc(AFNICommand):
    """
    For complete details, see the `to3d Documentation. 
    <http://afni.nimh.nih.gov/pub/dist/doc/program_help/3dcalc.html>`_
    """

    @property
    def cmd(self):
        """Base command for Threedcalc"""
        return '3dcalc'

    def inputs_help(self):
        doc = """
          Optional Parameters
          -------------------
        """
        print doc

    def _populate_inputs(self):
        """Initialize the inputs attribute."""

        self.inputs = Bunch(
            infile_a=None,
            expr=None,
            session=None,
            datum=None,
            outfile=None,
            )

    def _parseinputs(self):
        """Parse valid input options for Threedcalc command.

        Ignore options set to None.

        """

        out_inputs = []
        inputs = {}
        [inputs.update({k:v}) for k, v in self.inputs.iteritems() \
             if v is not None]

        if inputs.has_key('infile_a'):
            val = inputs.pop('infile_a')
            out_inputs.append('-a %s' % val)
        if inputs.has_key('expr'):
            val = inputs.pop('expr')
            out_inputs.append('-expr %s' % val)
        if inputs.has_key('session'):
            val = inputs.pop('session')
            out_inputs.append('-session %s' % val)
        if inputs.has_key('datum'):
            val = inputs.pop('datum')
            out_inputs.append('-datum %s' % val)
        if inputs.has_key('outfile'):
            val = inputs.pop('outfile')
            out_inputs.append('-prefix %s' % val)

        if len(inputs) > 0:
            print '%s: unsupported options: %s' % (
                self.__class__.__name__, inputs.keys())

        return out_inputs


class ThreedAllineate(AFNICommand):
    """
    For complete details, see the `to3d Documentation. 
    <http://afni.nimh.nih.gov/pub/dist/doc/program_help/3dAllineate.html>`_
    """

    @property
    def cmd(self):
        """Base command for ThreedAllineate"""
        return '3dAllineate'

    def inputs_help(self):
        doc = """
          Optional Parameters
          -------------------
        """
        print doc

    def _populate_inputs(self):
        """Initialize the inputs attribute."""

        self.inputs = Bunch(
            lpc=None,
            weight_frac=None,
            verbose=None,
            warp=None,
            maxrot=None,
            maxshf=None,
            source_automask=None,
            transform_matrix=None,
            base=None,
            weight=None,
            outfile=None,
            infile=None)

    def _parseinputs(self):
        """Parse valid input options for ThreedSkullStrip command.

        Ignore options set to None.

        """

        out_inputs = []
        inputs = {}
        [inputs.update({k:v}) for k, v in self.inputs.iteritems() \
             if v is not None]

        if inputs.has_key('lpc'):
            val = inputs.pop('lpc')
            out_inputs.append('-lpc')
        if inputs.has_key('weight_frac'):
            val = inputs.pop('weight_frac')
            out_inputs.append('-weight_frac %s' % str(val))
        if inputs.has_key('verbose'):
            val = inputs.pop('verbose')
            out_inputs.append('-VERB')
        if inputs.has_key('warp'):
            val = inputs.pop('warp')
            out_inputs.append('-warp %s' % val)
        if inputs.has_key('maxrot'):
            val = inputs.pop('maxrot')
            out_inputs.append('-maxrot %s' % str(val))
        if inputs.has_key('maxshf'):
            val = inputs.pop('maxshf')
            out_inputs.append('-maxshf %s' % str(val))
        if inputs.has_key('source_automask'):
            val = inputs.pop('source_automask')
            out_inputs.append('-source_automask+%s' % str(val))
        if inputs.has_key('transform_matrix'):
            val = inputs.pop('transform_matrix')
            out_inputs.append('-1Dmatrix_save %s' % val)
        if inputs.has_key('base'):
            val = inputs.pop('base')
            out_inputs.append('-base %s' % val)
        if inputs.has_key('weight'):
            val = inputs.pop('weight')
            out_inputs.append('-weight %s' % val)
        if inputs.has_key('outfile'):
            val = inputs.pop('outfile')
            out_inputs.append('-prefix %s' % val)
        if inputs.has_key('infile'):
            val = inputs.pop('infile')
            out_inputs.append('-source %s' % val)

        if len(inputs) > 0:
            print '%s: unsupported options: %s' % (
                self.__class__.__name__, inputs.keys())

        return out_inputs

