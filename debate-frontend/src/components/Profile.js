import React, { useState } from 'react';
import { axiosInstance } from '../config';
import '../styles/Profile.css';
import ProfileIcon from '../assets/icons/profile.svg';
import LogoutIcon from '../assets/icons/logout.svg';

const Profile = ({ user, setUser, resetDebate }) => {
    const [showGreeting, setShowGreeting] = useState(false);

    const handleLogout = async () => {
        try {
            await axiosInstance.post(`/logout`);
            resetDebate();
            setUser(null);
        } catch (error) {
            console.error('Logout failed', error);
        }
    };

    return (
        <div className="logout-profile-container">
            <div
                className="profile-icon"
                onMouseEnter={() => setShowGreeting(true)}
                onMouseLeave={() => setShowGreeting(false)}
            >
                <img src={ProfileIcon} alt="Profile Icon" className="h-6 w-6" />
                {showGreeting && <div className="greeting">Hi {user.username}</div>}
            </div>
            <div className="logout-icon" onClick={handleLogout}>
                <img src={LogoutIcon} alt="Logout Icon" className="h-6 w-6" />
                <div className="logout-text">Logout</div>
            </div>
        </div>
    );
};

export default Profile;