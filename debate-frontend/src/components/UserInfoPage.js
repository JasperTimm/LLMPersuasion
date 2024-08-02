// export default UserInfoPage;
import React, { useState } from 'react';
import { axiosInstance } from '../config';
import '../styles/UserInfoPage.css';

function UserInfoPage({ setUserInfoCompleted }) {
    const [age, setAge] = useState('');
    const [gender, setGender] = useState('');
    const [profession, setProfession] = useState('');
    const [introvertExtrovert, setIntrovertExtrovert] = useState('');
    const [error, setError] = useState('');
    const [personalityTraits, setPersonalityTraits] = useState({
        extravertedEnthusiastic: '',
        criticalQuarrelsome: '',
        dependableSelfDisciplined: '',
        anxiousEasilyUpset: '',
        openToExperiencesComplex: '',
        reservedQuiet: '',
        sympatheticWarm: '',
        disorganizedCareless: '',
        calmEmotionallyStable: '',
        conventionalUncreative: ''
    });
    const handlePersonalityTraitChange = (key, value) => {
        setPersonalityTraits({
            ...personalityTraits,
            [key]: value
        });
    };
    const handleSubmit = async () => {
        try {
            // Ensure all inputs are validated here
            const response = await axiosInstance.post('/user_info', {
                age,
                gender,
                profession,
                introvert_extrovert: introvertExtrovert,
                personality_traits: Object.values(personalityTraits)
            });

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

                      <div style={{ border: '1px solid black', padding: '10px', marginTop: '20px' }}>
                <p>Please write a number next to each statement to indicate the extent to which you agree or disagree with that statement. 
                    You should rate the extent to which the pair of traits applies to you, even if one characteristic applies more strongly than 
                    the other.
                    1 = Disagree strongly
                    2 = Disagree moderately
                    3 = Disagree a little
                    4 = Neither agree nor disagree
                    5 = Agree a little
                    6 = Agree moderately
                    7 = Agree strongly</p>
                <input
                    type="number"
                    value={personalityTraits.extravertedEnthusiastic}
                    onChange={(e) => handlePersonalityTraitChange('extravertedEnthusiastic', e.target.value)}
                    placeholder="Extraverted, enthusiastic"
                />
                <input
                    type="number"
                    value={personalityTraits.criticalQuarrelsome}
                    onChange={(e) => handlePersonalityTraitChange('criticalQuarrelsome', e.target.value)}
                    placeholder="Critical, quarrelsome"
                />
                <input
                    type="number"
                    value={personalityTraits.dependableSelfDisciplined}
                    onChange={(e) => handlePersonalityTraitChange('dependableSelfDisciplined', e.target.value)}
                    placeholder="Dependable, self-disciplined"
                />
                <input
                    type="number"
                    value={personalityTraits.anxiousEasilyUpset}
                    onChange={(e) => handlePersonalityTraitChange('anxiousEasilyUpset', e.target.value)}
                    placeholder="Anxious, easily upset"
                />
                <input
                    type="number"
                    value={personalityTraits.openToExperiencesComplex}
                    onChange={(e) => handlePersonalityTraitChange('openToExperiencesComplex', e.target.value)}
                    placeholder="Open to new experiences, complex"
                />
                <input
                    type="number"
                    value={personalityTraits.reservedQuiet}
                    onChange={(e) => handlePersonalityTraitChange('reservedQuiet', e.target.value)}
                    placeholder="Reserved, quiet"
                />
                <input
                    type="number"
                    value={personalityTraits.sympatheticWarm}
                    onChange={(e) => handlePersonalityTraitChange('sympatheticWarm', e.target.value)}
                    placeholder="Sympathetic, warm"
                />
                <input
                    type="number"
                    value={personalityTraits.disorganizedCareless}
                    onChange={(e) => handlePersonalityTraitChange('disorganizedCareless', e.target.value)}
                    placeholder="Disorganized, careless"
                />
                <input
                    type="number"
                    value={personalityTraits.calmEmotionallyStable}
                    onChange={(e) => handlePersonalityTraitChange('calmEmotionallyStable', e.target.value)}
                    placeholder="Calm, emotionally stable"
                />
                <input
                    type="number"
                    value={personalityTraits.conventionalUncreative}
                    onChange={(e) => handlePersonalityTraitChange('conventionalUncreative', e.target.value)}
                    placeholder="Conventional, uncreative"
                />
            </div>
            <button onClick={handleSubmit}>Submit</button>
        </div>
    );
}

export default UserInfoPage;

