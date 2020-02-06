import React from 'react';
import { render } from 'react-dom';

import 'bootstrap-css-only/css/bootstrap.min.css';

import '../css/treeherder-global.css';
import '../css/treeherder-userguide.css';
import '../css/treeherder-job-buttons.css';

import App from './App';

render(<App />, document.getElementById('root'));
