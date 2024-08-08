import React, { useState } from 'react';
import '../styles/UserInfoPage.css';

function DemographicsPage({ setDemographics }) {
    const [age, setAge] = useState('');
    const [gender, setGender] = useState('');
    const [profession, setProfession] = useState('');
    const [educationLevel, setEducationLevel] = useState('');
    const [countryMostTime, setCountryMostTime] = useState('');

    const handleNext = () => {
        setDemographics({ age, gender, profession, educationLevel, countryMostTime });
    };

    return (
        <div className="container">
            <h2>Demographics</h2>
            <input
                type="number"
                value={age}
                onChange={(e) => setAge(e.target.value)}
                placeholder="Age"
            />
            <input
                type="text"
                value={gender}
                onChange={(e) => setGender(e.target.value)}
                placeholder="Gender"
            />
            <input
                type="text"
                value={profession}
                onChange={(e) => setProfession(e.target.value)}
                placeholder="Profession"
            />
            <input
                type="text"
                value={educationLevel}
                onChange={(e) => setEducationLevel(e.target.value)}
                placeholder="Education Level"
            />
            <input
                type="text"
                value={countryMostTime}
                onChange={(e) => setCountryMostTime(e.target.value)}
                placeholder="Country Most Time"
            />
            <button onClick={handleNext}>Next</button>
        </div>
    );
}

export default DemographicsPage;