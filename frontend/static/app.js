const $ = id => document.getElementById(id);

$('saving_percentage').addEventListener('input', e => {
  $('saveValue').textContent = e.target.value + '%';
});

function money(x) {
  return '₹' + Number(x || 0).toLocaleString('en-IN', { maximumFractionDigits: 0 });
}

function pick(obj, ...keys) {
  for (const k of keys) {
    if (obj && obj[k] !== undefined && obj[k] !== null) return obj[k];
  }
  return 0;
}

function statusClass(status) {
  const value = String(status || '').toLowerCase();
  if (value === 'achievable') return 'good';
  if (value === 'challenging') return 'warn';
  return 'bad';
}

function renderGoal(key, label, icon, goal, recommendation) {
  const current = pick(goal, 'current_cost');
  const future = pick(goal, 'future_cost');
  const monthly = pick(goal, 'monthly_investment');
  const years = pick(goal, 'years');
  const goalStatus = pick(goal, 'status') || 'Not available';
  const category = recommendation?.broad_category || 'Educational category guidance';

  return `
    <article class="result-goal-card">
      <div class="result-goal-header">
        <div class="result-goal-title">
          <span class="result-goal-icon">${icon}</span>
          <div>
            <h3>${label}</h3>
            <span class="result-goal-timeline">${years} years</span>
          </div>
        </div>
        <span class="goal-status ${statusClass(goalStatus)}">${goalStatus}</span>
      </div>

      <div class="result-goal-details">
        <div class="result-detail">
          <span>Current cost</span>
          <strong>${money(current)}</strong>
        </div>
        <div class="result-detail">
          <span>Future cost</span>
          <strong>${money(future)}</strong>
        </div>
        <div class="result-detail result-detail-full">
          <span>Monthly investment required</span>
          <strong>${money(monthly)}</strong>
        </div>
      </div>

      <div class="recommendation-box">
        <span>Recommended category</span>
        <strong>${category}</strong>
      </div>
    </article>`;
}

$('plannerForm').addEventListener('submit', async e => {
  e.preventDefault();

  $('message').innerHTML = '';
  $('results').classList.add('hidden');

  const payload = {
    name: $('name').value.trim(),
    age: Number($('age').value),
    city: $('city').value.trim(),
    education: $('education').value.trim(),
    job_role: $('job_role').value.trim(),
    monthly_salary: Number($('monthly_salary').value),
    marriage_years: Number($('marriage').value),
    car_years: Number($('car').value),
    home_years: Number($('home').value),
    saving_percent: Number($('saving_percentage').value),
    area_type: $('area_type').value || null
  };

  const btn = document.querySelector('.primary');
  btn.disabled = true;
  btn.textContent = 'Calculating...';

  try {
    const response = await fetch('/plan', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(payload)
    });

    const data = await response.json();

    if (!response.ok) {
      let message = data?.detail || 'Could not generate the plan.';
      if (Array.isArray(message)) {
        message = message.map(x => `${x.loc?.join(' → ') || 'field'}: ${x.msg}`).join('<br>');
      }
      throw new Error(typeof message === 'string' ? message : JSON.stringify(message));
    }

    const salary = pick(data, 'entered_monthly_salary', 'monthly_salary');
    const capacity = pick(data, 'available_monthly_investment');
    const required = pick(data, 'total_required_monthly_investment');
    const surplus = pick(data, 'surplus');
    const shortfall = pick(data, 'shortfall');

    $('salary').textContent = money(salary);
    $('capacity').textContent = money(capacity);
    $('capacity').dataset.value = capacity;
    $('required').textContent = money(required);
    $('gap').textContent = shortfall > 0 ? '- ' + money(shortfall) : '+ ' + money(surplus);

    const status = data.feasibility || 'Plan generated';
    $('status').className = 'status ' + statusClass(status);
    $('status').innerHTML = `Overall feasibility: ${status}`;

    const goals = data.goals || {};
    const recs = data.recommendations || {};

    $('goalCards').innerHTML =
      renderGoal('marriage', 'Marriage', '💍', goals.marriage || {}, recs.marriage) +
      renderGoal('car', 'Car', '🚗', goals.car || {}, recs.car) +
      renderGoal('home', 'Home', '🏠', goals.home || {}, recs.home);

    if (shortfall > 0 && Array.isArray(recs.gap_actions)) {
      $('status').innerHTML += '<br><small>Ways to reduce the gap: ' + recs.gap_actions.join(' • ') + '</small>';
    }

    $('results').classList.remove('hidden');
    $('results').scrollIntoView({behavior: 'smooth'});
  } catch (err) {
    $('message').innerHTML = `<div class="error"><strong>Could not generate the plan.</strong><br>${err.message}</div>`;
  } finally {
    btn.disabled = false;
    btn.textContent = 'Generate my financial plan →';
  }
});
