# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileCopyrightText: 2016 Triplus
# SPDX-FileNotice: Part of the Runner addon.

from .Cleanup import removeExisting
from .Dock import registerDock


removeExisting()
registerDock()
