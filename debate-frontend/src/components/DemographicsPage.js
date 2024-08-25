import React, { useState } from 'react';
import '../styles/UserInfoPage.css';

function DemographicsPage({ setDemographics }) {
    const [age, setAge] = useState('');
    const [gender, setGender] = useState('');
    const [profession, setProfession] = useState('');
    const [educationLevel, setEducationLevel] = useState('');
    const [countryMostTime, setCountryMostTime] = useState('');
    const [error, setError] = useState('');

    const isFormValid = () => {
        return age !== '' && gender !== '' && profession !== '' && educationLevel !== '' && countryMostTime !== '';
    };

    const handleNext = () => {
        if (!isFormValid()) {
            setError('Please fill out all fields.');
            return;
        }
        setDemographics({ age, gender, profession, educationLevel, countryMostTime });
    };

    const countries = [
"Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", 
"Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", 
"Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", 
"Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", 
"Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", 
"Canada", "Central African Republic", "Chad", "Chile", "China", "Colombia", 
"Comoros", "Congo (Congo-Brazzaville)", "Costa Rica", "Croatia", "Cuba", "Cyprus", 
"Czech Republic", "Democratic Republic of the Congo", "Denmark", "Djibouti", 
"Dominica", "Dominican Republic", "Ecuador", "Egypt", "El Salvador", 
"Equatorial Guinea", "Eritrea", "Estonia", "Eswatini (fmr. Swaziland)", 
"Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", 
"Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", 
"Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", 
"Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", 
"Kazakhstan", "Kenya", "Kiribati", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", 
"Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", 
"Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", 
"Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", 
"Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", 
"Myanmar (formerly Burma)", "Namibia", "Nauru", "Nepal", "Netherlands", 
"New Zealand", "Nicaragua", "Niger", "Nigeria", "North Korea", "North Macedonia", 
"Norway", "Oman", "Pakistan", "Palau", "Palestine", "Panama", "Papua New Guinea", 
"Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", 
"Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", 
"Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal", 
"Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", 
"Solomon Islands", "Somalia", "South Africa", "South Korea", "South Sudan", 
"Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", 
"Taiwan", "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo", 
"Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", 
"Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States of America", 
"Uruguay", "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela", "Vietnam", 
"Yemen", "Zambia", "Zimbabwe"

    ];

    return (
        <div className="container">
            <h2>Demographics</h2>
            <input
                type="number"
                value={age}
                onChange={(e) => setAge(e.target.value)}
                placeholder="Age"
            />
            <select value={gender} onChange={(e) => setGender(e.target.value)}>
                <option value="" disabled>Select Gender</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Others">Others</option>
            </select>
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
            <select
            value={countryMostTime}
            onChange={(e) => setCountryMostTime(e.target.value)}
            style={{ color: countryMostTime === "" ? "#a9a9a9" : "#000" }}
            onBlur={(e) => e.target.style.color = countryMostTime === "" ? "#a9a9a9" : "#000"}
            >
            <option value="" disabled hidden>Country you've lived the longest in</option>
            {countries.map((country, index) => (
                <option key={index} value={country} style={{ color: "#000" }}>
                {country}
                </option>
            ))}
            </select>
            <button onClick={handleNext}>Next</button>
            {error && <p className="error">{error}</p>}
                        
        </div>
    );
}

export default DemographicsPage;
