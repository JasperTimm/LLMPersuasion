import React from 'react';
import { axiosInstance } from '../config';
import '../styles/EndEarlyPage.css';

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
            <div className="button-group">
                <button onClick={handleConfirm} className="button">Confirm</button>
                <button onClick={handleCancel} className="button">Cancel</button>
            </div>
        </div>
    );
};

export default EndEarlyPage;