/* eslint-disable jsx-a11y/no-noninteractive-element-interactions */

import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import {
  Label,
  DropdownMenu,
  DropdownItem,
  DropdownToggle,
  UncontrolledDropdown,
} from 'reactstrap';
import { faCheck } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

import { thAllResultStatuses } from '../../helpers/constants';
import { getJobsUrl } from '../../helpers/url';
import { setSelectedJob, clearSelectedJob } from '../redux/stores/selectedJob';
import { pinJobs } from '../redux/stores/pinnedJobs';

const resultStatusMenuItems = thAllResultStatuses.filter(
  rs => rs !== 'runnable',
);

function FiltersMenu(props) {
  const {
    filterModel,
    pinJobs,
    getAllShownJobs,
    selectedJob,
    setSelectedJob,
    user,
  } = props;
  const {
    urlParams: { resultStatus, classifiedState },
  } = filterModel;

  const pinAllShownJobs = () => {
    const shownJobs = getAllShownJobs();

    pinJobs(shownJobs);
    if (!selectedJob) {
      setSelectedJob(shownJobs[0]);
    }
  };
  const { email } = user;

  return (
    <UncontrolledDropdown>
      <DropdownToggle
        title="Set filters"
        className="btn-view-nav nav-menu-btn"
        nav
        caret
      >
        Filters
      </DropdownToggle>
      <DropdownMenu>
        {resultStatusMenuItems.map(filterName => (
          <DropdownItem
            key={filterName}
            tag="a"
            onClick={() => filterModel.toggleResultStatuses([filterName])}
          >
            <FontAwesomeIcon
              icon={faCheck}
              className={`mr-1 ${
                resultStatus.includes(filterName) ? '' : 'hide'
              }`}
              title={resultStatus.includes(filterName) ? 'Selected' : ''}
            />
            {filterName}
          </DropdownItem>
        ))}
        <div className="dropdown-divider separator" />
        <DropdownItem tag="a">
          <Label className="dropdown-item">
            <input
              type="checkbox"
              id="classified"
              checked={classifiedState.includes('classified')}
              onChange={() => filterModel.toggleClassifiedFilter('classified')}
            />
            classified
          </Label>
        </DropdownItem>
        <DropdownItem tag="a">
          <Label className="dropdown-item">
            <input
              type="checkbox"
              id="unclassified"
              checked={classifiedState.includes('unclassified')}
              onChange={() =>
                filterModel.toggleClassifiedFilter('unclassified')
              }
            />
            unclassified
          </Label>
        </DropdownItem>
        <li className="dropdown-divider separator" />
        <li
          title="Pin all jobs that pass the global filters"
          className="dropdown-item"
          onClick={pinAllShownJobs}
        >
          Pin all showing
        </li>
        <li
          title="Show only superseded jobs"
          className="dropdown-item"
          onClick={filterModel.setOnlySuperseded}
        >
          Superseded only
        </li>
        <li title={`Show only pushes for ${email}`} className="dropdown-item">
          <a href={getJobsUrl({ author: email })}>My pushes only</a>
        </li>
        <li
          title="Reset to default status filters"
          className="dropdown-item"
          onClick={filterModel.resetNonFieldFilters}
        >
          Reset
        </li>
      </DropdownMenu>
    </UncontrolledDropdown>
  );
}

FiltersMenu.propTypes = {
  filterModel: PropTypes.object.isRequired,
  pinJobs: PropTypes.func.isRequired,
  setSelectedJob: PropTypes.func.isRequired,
  getAllShownJobs: PropTypes.func.isRequired,
  selectedJob: PropTypes.object,
  user: PropTypes.object.isRequired,
};

FiltersMenu.defaultProps = {
  selectedJob: null,
};

const mapStateToProps = ({ selectedJob: { selectedJob } }) => ({ selectedJob });

export default connect(mapStateToProps, {
  setSelectedJob,
  clearSelectedJob,
  pinJobs,
})(FiltersMenu);
