select *
from CovidDeaths
where continent is not null
order by 3,4

--select *
--from CovidVaccinations
--order by 3,4

select location, date, total_cases, new_cases, total_deaths, population
from CovidDeaths
order by 1,2

-- total cases vs total deaths
-- shows the likelihood of dying by country and date

select location, date, total_cases,  total_deaths, (total_deaths/total_cases)*100 as DeathRatePercentage
from CovidDeaths
where location like '%states'
order by 1,2

--total cases vs population
--shows what percentage of population has covid

select location, date, population, total_cases,  (total_cases/population)*100
from CovidDeaths
where location like 'nigeria'
order by 1,2

--looking at countries with highest infection rate

select location, population, max(total_cases) as highestinfectedcount,  max((total_cases/population))*100 as infectedpercentage
from CovidDeaths
group by location, population
order by infectedpercentage desc

-- shows countries with the highest count of death per population

select location, MAX(cast(total_deaths as int)) as maxdeaths 
From CovidDeaths
where continent is not null
group by location
order by maxdeaths desc

-----by continent
select continent, MAX(cast(total_deaths as int)) as maxdeaths 
From CovidDeaths
where continent is not null
group by continent
order by maxdeaths desc

--GLOBAL NUMBERS

select sum(new_cases) as total_cases,  sum(cast(new_deaths as int)) as total_deaths, sum(cast(new_deaths as int))/sum(new_cases)*100 as DeathRatePercentage
from CovidDeaths
where continent is not null
--group by date
order by 1,2

--looking at total population vs vaccination

select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations, 
sum(convert(int, vac.new_vaccinations)) OVER (partition by dea.location order by dea.location, dea.date) as rollingvaccinated
from CovidDeaths dea
join CovidVaccinations vac
	on dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null
order by 2,3

-- CTE 

with popvsvac (continent, location, date, populations, new_vaccinations, rollingvaccinated)
as
(
select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations, 
sum(convert(int, vac.new_vaccinations)) OVER (partition by dea.location order by dea.location, dea.date) as rollingvaccinated
from CovidDeaths dea
join CovidVaccinations vac
	on dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null
--order by 2,3
)
select *, (rollingvaccinated/populations)*100 as percentpopulationvaccinated
from popvsvac

-- temp table

drop table if exists #percentpeoplevaccinated
create table #percentpeoplevaccinated
(
Continent nvarchar(255),
Location nvarchar(255),
Date datetime,
Population numeric,
New_vaccinations numeric,
Rollingvaccinated numeric
)

insert into #percentpeoplevaccinated
select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations, 
sum(convert(int, vac.new_vaccinations)) OVER (partition by dea.location order by dea.location, dea.date) as rollingvaccinated
from CovidDeaths dea
join CovidVaccinations vac
	on dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null
--order by 2,3

select *, (rollingvaccinated/population)*100 as percentpopulationvaccinated
from #percentpeoplevaccinated


-- creating view for later

create view  percentpopulationvaccinated as 
select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations, 
sum(convert(int, vac.new_vaccinations)) OVER (partition by dea.location order by dea.location, dea.date) as rollingvaccinated
from CovidDeaths dea
join CovidVaccinations vac
	on dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null
--order by 2,3

select *
from  percentpopulationvaccinated

--another view

create view globalnumbers as
select sum(new_cases) as total_cases,  sum(cast(new_deaths as int)) as total_deaths, sum(cast(new_deaths as int))/sum(new_cases)*100 as DeathRatePercentage
from CovidDeaths
where continent is not null
--order by 1,2

select *
from globalnumbers

--another view

create view totaldeathspercontinents as
select continent, sum(cast(new_deaths as int)) as totaldeaths 
From CovidDeaths
where continent is not null
and location not in ('world', 'european union', 'international') 
group by continent
--order by totaldeaths desc

--another view

create view infectedpercentagepercountry as
select location, population, max(total_cases) as highestinfectedcount,  max((total_cases/population))*100 as infectedpercentage
from CovidDeaths
where continent is not null
group by location, population
order by infectedpercentage desc

--
create view infectedpercentage as
select location, population,date,  max(total_cases) as highestinfectedcount,  max((total_cases/population))*100 as infectedpercentage
from CovidDeaths
group by location, population,date
order by infectedpercentage asc





--cooking
create view damola as
select continent, location, date, population, total_cases, total_deaths
from CovidDeaths
where continent is not null
order by 2,3
























