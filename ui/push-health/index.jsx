import React from 'react';
import { render } from 'react-dom';

// Vendor Styles
import 'bootstrap-css-only/css/bootstrap.min.css';

// Treeherder Styles
import '../css/treeherder-navbar.css';
import '../css/treeherder-job-buttons.css';
import '../css/treeherder-notifications.css';
import './pushhealth.css';

import App from './App';

render(<App />, document.getElementById('root'));
