kraken
======

.. toctree::
   :hidden:
   :maxdepth: 2

   advanced
   Training <ketos>
   API Tutorial <api>
   API Reference <api_docs>
   Models <models>

kraken is a turn-key OCR system optimized for historical and non-Latin script
material.

Features
========

kraken's main features are:

  - Fully trainable layout analysis and character recognition
  - `Right-to-Left <https://en.wikipedia.org/wiki/Right-to-left>`_, `BiDi
    <https://en.wikipedia.org/wiki/Bi-directional_text>`_, and Top-to-Bottom
    script support
  - `ALTO <https://www.loc.gov/standards/alto/>`_, PageXML, abbyXML, and hOCR
    output
  - Word bounding boxes and character cuts
  - Multi-script recognition support
  - `Public repository <https://zenodo.org/communities/ocr_models>`_ of model files
  - :ref:`Lightweight model files <models>`
  - :ref:`Variable recognition network architectures <vgsl>`

Pull requests and code contributions are always welcome. 

Installation
============

Kraken can be run on Linux or Mac OS X (both x64 and ARM). Installation through
the on-board *pip* utility and the `anaconda <https://anaconda.org>`_
scientific computing python are supported.

Installation using Pip
----------------------

.. code-block:: console

  $ pip install kraken

or by running pip in the git repository:

.. code-block:: console

  $ pip install .

If you want direct PDF and multi-image TIFF/JPEG2000 support it is necessary to
install the `pdf` extras package for PyPi:

.. code-block:: console

   $ pip install kraken[pdf]

or

.. code-block:: console

   $ pip install .[pdf]

respectively.

Installation using Conda
------------------------

To install the stable version through `conda <https://anaconda.org>`_:

.. code-block:: console

   $ conda install -c conda-forge -c mittagessen kraken

Again PDF/multi-page TIFF/JPEG2000 support requires some additional dependencies:

.. code-block:: console

   $ conda install -c conda-forge pyvips

The git repository contains some environment files that aid in setting up the latest development version:


.. code-block:: console

  $ git clone git://github.com/mittagessen/kraken.git 
  $ cd kraken
  $ conda env create -f environment.yml

or:

.. code-block:: console

  $ git clone git://github.com/mittagessen/kraken.git 
  $ cd kraken
  $ conda env create -f environment_cuda.yml

for CUDA acceleration with the appropriate hardware.

Finding Recognition Models
--------------------------

Finally you'll have to scrounge up a recognition model to do the actual
recognition of characters. To download the default English text recognition
model and place it in the user's kraken directory:

.. code-block:: console

  $ kraken get 10.5281/zenodo.2577813

A list of libre models available in the central repository can be retrieved by
running:

.. code-block:: console

  $ kraken list

Model metadata can be extracted using:

.. code-block:: console

  $ kraken show 10.5281/zenodo.2577813
  name: 10.5281/zenodo.2577813

  A generalized model for English printed text
  
  This model has been trained on a large corpus of modern printed English text\naugmented with ~10000 lines of historical p
  scripts: Latn
  alphabet: !"#$%&'()+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]`abcdefghijklmnopqrstuvwxyz{} SPACE
  accuracy: 99.95%
  license: Apache-2.0
  author(s): Kiessling, Benjamin
  date: 2019-02-26

Quickstart
==========

Recognizing text on an image using the default parameters including the
prerequisite steps of binarization and page segmentation:

.. code-block:: console

  $ kraken -i image.tif image.txt segment -bl ocr
  Loading RNN     ✓
  Processing      ⣻

To binarize a single image using the nlbin algorithm (usually not required with the baseline segmenter):

.. code-block:: console

  $ kraken -i image.tif bw.tif binarize

To segment a binarized image into reading-order sorted baselines and regions:

.. code-block:: console

  $ kraken -i bw.tif lines.json segment -bl

To OCR an image using the default RNN:

.. code-block:: console

  $ kraken -i bw.tif image.txt segment -bl ocr

All commands and their parameters are documented, just add the standard
``--help`` flag for further information.

Training Tutorial
=================

There is a training tutorial at :doc:`training`.

.. _license:

License
=======

``Kraken`` is provided under the terms and conditions of the `Apache 2.0
License <https://github.com/mittagessen/kraken/blob/master/LICENSE>`_.

Funding
=======

kraken is developed at the `École Pratique des Hautes Études <http://ephe.fr>`_, `Université PSL <http://www.psl.eu>`_.

This project was partially funded through the RESILIENCE project, funded from
the European Union’s Horizon 2020 Framework Programme for Research and
Innovation.

.. image:: https://ec.europa.eu/regional_policy/sources/information/logos_downloadcenter/eu_funded_en.jpg
  :alt: Co-financed by the European Union

