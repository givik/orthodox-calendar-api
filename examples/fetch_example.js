/**
 * Example of fetching Orthodox liturgical calendar data in JavaScript / TypeScript.
 * Compatible with Node.js 18+, browsers, React, React Native, Vue, etc.
 */

async function fetchCalendarDay(dateStr = '2026-10-14', lang = 'ka') {
  const url = `http://localhost:8000/api/v1/day?date=${dateStr}&lang=${lang}`;
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    console.log('--- Orthodox Liturgical Day ---');
    console.log(`გრიგორიანული თარიღი: ${data.gregorian_date} (${data.weekday.name})`);
    console.log(`ძველი სტილით (იულიუსის): ${data.julian_date}`);
    console.log(`დღესასწაული: ${data.title}`);
    console.log(`მარხვა: ${data.fasting.name} - ${data.fasting.description}`);
    console.log('წმინდანები:');
    data.saints.forEach(saint => console.log(`  * ${saint}`));
    return data;
  } catch (error) {
    console.error('Error fetching calendar:', error);
  }
}

// Execute
fetchCalendarDay();
