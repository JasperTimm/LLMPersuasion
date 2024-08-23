import React from 'react';
import { axiosInstance } from '../config';

const EndEarlyPage = ({ setEndEarly, user, setUser }) => {

    const handleConfirm = async () => {
        try {
            await axiosInstance.post(`/finish`);
            setUser({ ...user, finished: true });
            setEndEarly(false);
        } catch (error) {
            console.error('Error finishing participation:', error);
        }
    };

    const handleCancel = () => {
        setEndEarly(false);
    };

    return (
        <div className="container">
            <h1>End Participation</h1>
            <p>
                By ending your participation, you will not be able to participate in any further debates.
                Are you sure you want to end your participation?
            </p>
            <button onClick={handleConfirm} style={{ marginRight: '10px' }}>Confirm</button>
            <button onClick={handleCancel} style={{ marginLeft: '10px' }}>Cancel</button>
        </div>
    );
};

export default EndEarlyPage;