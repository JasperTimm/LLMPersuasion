// export default UserInfoPage;
import React, { useState } from 'react';
import { axiosInstance } from '../config';
import '../styles/UserInfoPage.css';

function UserInfoPage({ setUserInfoCompleted }) {
    const [age, setAge] = useState('');
    const [gender, setGender] = useState('');
    const [profession, setProfession] = useState('');
    const [introvertExtrovert, setIntrovertExtrovert] = useState('');

    const handleSubmit = async () => {
        try {
            const response = await axiosInstance.post('/user_info', { age, gender, profession, introvertExtrovert });
            if (response.status === 200) {
                setUserInfoCompleted(true);
            }
        } catch (error) {
            console.error('Error submitting user info:', error);
        }
    };

    return (
        <div className="container">
            <h2>User Information</h2>
            <input
                type="number"
                value={age}
                onChange={(e) => setAge(e.target.value)}
                placeholder="Enter your age"
            />
            <select
                value={gender}
                onChange={(e) => setGender(e.target.value)}
            >
                <option value="">Select Gender</option>
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="other">Other</option>
            </select>
            <input
                type="text"
                value={profession}
                onChange={(e) => setProfession(e.target.value)}
                placeholder="Enter your profession"
            />
            <select
                value={introvertExtrovert}
                onChange={(e) => setIntrovertExtrovert(e.target.value)}
            >
                <option value="">Select Introvert/Extrovert</option>
                <option value="introvert">Introvert</option>
                <option value="extrovert">Extrovert</option>
            </select>
            <button onClick={handleSubmit}>Submit</button>
        </div>
    );
}

export default UserInfoPage;
