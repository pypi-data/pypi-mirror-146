#!/bin/bash

# Copyright (C) 2019 Tobias Jakobi
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

tail -n +2  $1 | awk -F '\t' '{if ($6<0.05 && $13 > 0.05){print $1"\t"$2"\t"$3"\t"$4"\t"$6"\t"$8"\t"$13"\t"$15}}' | sort -nrk6,6