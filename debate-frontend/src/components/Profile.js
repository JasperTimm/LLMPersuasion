import React, { useState, useEffect, useRef } from 'react';
import { axiosInstance } from '../config';
import '../styles/Profile.css';
import ProfileIcon from '../assets/icons/profile.svg';
import LogoutIcon from '../assets/icons/logout.svg';

const Profile = ({ user, setUser, resetDebate, setEndEarly }) => {
    const [showGreeting, setShowGreeting] = useState(false);
    const [showMenu, setShowMenu] = useState(false);
    const menuRef = useRef(null);

    const handleLogout = async () => {
        try {
            await axiosInstance.post(`/logout`);
            resetDebate();
            setUser(null);
        } catch (error) {
            console.error('Logout failed', error);
        }
    };

    const handleEndParticipation = () => {
        setEndEarly(true);
        setShowMenu(false);
    };

    const handleClickOutside = (event) => {
        if (menuRef.current && !menuRef.current.contains(event.target)) {
            setShowMenu(false);
        }
    };

    useEffect(() => {
        if (showMenu) {
            document.addEventListener('mousedown', handleClickOutside);
        } else {
            document.removeEventListener('mousedown', handleClickOutside);
        }

        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, [showMenu]);

    return (
        <div className="logout-profile-container">
            <div
                className="profile-icon"
                onMouseEnter={() => setShowGreeting(true)}
                onMouseLeave={() => setShowGreeting(false)}
                onClick={() => setShowMenu(!showMenu)}
            >
                <img src={ProfileIcon} alt="Profile Icon" className="h-6 w-6" />
                {showGreeting && <div className="greeting">Profile</div>}
            </div>
            {showMenu && (
                <div className="profile-menu" ref={menuRef}>
                    <div className="menu-item username"><strong>{user.username}</strong></div>
                    <hr />
                    {user.volunteer && (
                        <div className="menu-item" onClick={handleEndParticipation}>
                            End Participation
                        </div>
                    )}
                    <hr />
                    <div className="menu-item" onClick={handleLogout}>
                        <img src={LogoutIcon} alt="Logout Icon" className='logout-icon' />
                        Logout
                    </div>
                </div>
            )}
        </div>
    );
};

export default Profile;