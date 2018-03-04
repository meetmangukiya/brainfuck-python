python-brainfuck a.k.a brainfucky
=================================

Brainfucky is a brainfuck interpreter written in python.

About Brainfuck
---------------

Brainfuck is an esoteric programming language. The language has only 8 symbols,
each performing certain functions, see below.

+-----+-------------------------------------------------------------------------+
|``+``| Increment the value of current cell by 1.                               |
+-----+-------------------------------------------------------------------------+
|``-``| Decrement the value of current cell by 1.                               |
+-----+-------------------------------------------------------------------------+
|``>``| Move the current cell pointer to right, increment the pointer by 1.     |
+-----+-------------------------------------------------------------------------+
|``<``| Move the current cell pointer to left, decrement the pointer by 1.      |
+-----+-------------------------------------------------------------------------+
|``.``| Print the ascii character corresponding to the value of current cell.   |
+-----+-------------------------------------------------------------------------+
|``,``| Take an ascii input from user, and store its ascii value in current cell|
+-----+-------------------------------------------------------------------------+
|``[``| if the byte at the data pointer is zero, then instead of moving the     |
|     | instruction pointer forward to the next command, jump it forward to     |
|     | the command after the matching ``]`` command.                           |
+-----+-------------------------------------------------------------------------+
|``]``| if the byte at the data pointer is nonzero, then instead of moving the  |
|     | instruction pointer forward to the next command, jump it back to the    |
|     | command after the matching ``[`` command.                               |
+-----+-------------------------------------------------------------------------+

About Implementation
--------------------

- The memory element, the tape is emulated using the python ``list``.
- Value of ith element in the list corresponds to the value of cell ``i``.
- A cell pointer is used to point towards the current cell.
- ``+`` and ``-`` increments the value of cell pointed by the cell pointer.
- ``>`` and ``<`` increments and decrements the cell pointer effectively, moving
  the tape right or left.
- Instructions in a block are executed and at the end of the execution of last
  instruction, value of current cell is checked, if it is 0, move on, else
  execute the block again.

Install
-------

.. code:: bash

   $ pip install brainfucky

Run
---

To run your brainfuck program do the following

.. code:: bash

   $ brainfucky --file examples/hello_world.bf
   executing file examples/hello_world.bf
   Hello World!

   $ brainfucky --file examples/triangle.bf
   executing file examples/triangle.bf
                                  *
                                 * *
                                *   *
                               * * * *
                              *       *
                             * *     * *
                            *   *   *   *
                           * * * * * * * *
                          *               *
                         * *             * *
                        *   *           *   *
                       * * * *         * * * *
                      *       *       *       *
                     * *     * *     * *     * *
                    *   *   *   *   *   *   *   *
                   * * * * * * * * * * * * * * * *
                  *                               *
                 * *                             * *
                *   *                           *   *
               * * * *                         * * * *
              *       *                       *       *
             * *     * *                     * *     * *
            *   *   *   *                   *   *   *   *
           * * * * * * * *                 * * * * * * * *
          *               *               *               *
         * *             * *             * *             * *
        *   *           *   *           *   *           *   *
       * * * *         * * * *         * * * *         * * * *
      *       *       *       *       *       *       *       *
     * *     * *     * *     * *     * *     * *     * *     * *
    *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *
   * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
