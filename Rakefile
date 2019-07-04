task :default => [:run_server]


task :check_django_environment do
  abort "Set DJANGO_ENV variable! via export DJANGO_ENV=..." unless ENV['DJANGO_ENV']
end


task :check_development_environment => [:check_django_environment] do
  abort "Set DJANGO_ENV to development" unless ENV['DJANGO_ENV'] == 'development'
end


desc "Run server"
task :run_server => [:check_development_environment] do
  system "DJANGO_COLORS='dark' python manage.py runserver_plus --nothreading"
end


AVAILABLE_REPLS = ["ptpython", "ipython", "bpython"]
desc "Run shell+ avail: #{AVAILABLE_REPLS.join(',')} default: #{AVAILABLE_REPLS.first}"
task :shell, [:repl] => [:check_development_environment]  do |_, args|
  args.with_defaults(:repl => AVAILABLE_REPLS.first)
  abort "Please provide valid repl: #{AVAILABLE_REPLS.join(',')}" unless AVAILABLE_REPLS.include?(args.repl)
  system "python manage.py shell_plus --print-sql --#{args.repl}"
end


namespace :new do
  desc "Create new Django application"
  task :application, [:name_of_application] => [:check_development_environment] do |_, args|
    abort "Please provide: 'name_of_application'" unless args.name_of_application
    
    system "python manage.py create_app #{args.name_of_application}"
  end


  AVAILABLE_MODEL_TYPES = ['django', 'basemodel', 'softdelete']
  desc "Create new Model for given application: #{AVAILABLE_MODEL_TYPES.join(',')}"
  task :model, [:name_of_application, :name_of_model, :type_of_model] => [:check_development_environment] do |_, args|
    args.with_defaults(:type_of_model => "django")
    abort "Please provide: 'name_of_application'" unless args.name_of_application
    abort "Please provide: 'name_of_model'" unless args.name_of_model
    abort "Please provide valid model type: #{AVAILABLE_MODEL_TYPES.join(',')}" unless AVAILABLE_MODEL_TYPES.include?(args.type_of_model)
    
    system "python manage.py create_model #{args.name_of_application} #{args.name_of_model} #{args.type_of_model}"
  end
end


namespace :locale do
  desc "Update locale dictionary"
  task :update => [:check_development_environment] do
    system "python manage.py makemessages -a -s --ignore=htmlcov -v 2"
    system "python manage.py makemessages -a -s -d djangojs --ignore=htmlcov -v 2"
  end


  desc "Compile locale dictionary"
  task :compile => [:check_development_environment] do
    system "python manage.py compilemessages"
  end
end


namespace :db do
  desc "Run migration for given database (default: 'default')"
  task :migrate, [:database] => [:check_development_environment] do |_, args|
    args.with_defaults(:database => "default")
    puts "Running migration for: #{args.database} database..."
    system "python manage.py migrate --database=#{args.database}"
  end


  desc "run database shell ..."
  task :shell => [:check_development_environment] do
    system "python manage.py dbshell"
  end
  

  desc "Show migrations for an application (default: 'all')"
  task :show, [:name_of_application] => [:check_development_environment] do |_, args|
    args.with_defaults(:name_of_application => "all")
    single_application_or_all = " #{args.name_of_application}"
    single_application_or_all = "" if args.name_of_application == "all"
    system "python manage.py showmigrations#{single_application_or_all}"
  end


  desc "Update migration (name of application, name of migration?, is empty?)"
  task :update, [:name_of_application, :name_of_migration, :is_empty] => [:check_development_environment] do |_, args|
    abort "Please provide: 'name_of_application'" unless args.name_of_application

    args.with_defaults(:name_of_migration => "auto_#{Time.now.strftime('%Y%m%d_%H%M')}")
    args.with_defaults(:is_empty => "no")
    name_param = "--name #{args.name_of_migration}"
    empty_param = ""
    unless args.is_empty == "no"
      empty_param = "--empty #{args.name_of_application} "
    end
    system "python manage.py makemigrations #{empty_param}#{name_param}"
  end

  
  desc "Roll-back (name of application, name of migration)"
  task :roll_back, [:name_of_application, :name_of_migration] => [:check_development_environment] do |_, args|
    abort "Please provide: 'name_of_application'" unless args.name_of_application
    args.with_defaults(:name_of_migration => nil)
    which_application = args.name_of_application
    which_application = "" if args.name_of_application == "all"
    if args.name_of_migration.nil?
      puts "Please select your migration:"
      system "python manage.py showmigrations #{which_application}"
    else
      system "python manage.py migrate #{which_application} #{sprintf("%04d", args.name_of_migration)}"
    end
  end
end



namespace :test do
  desc "Run tests for given application. (default: 'applications' tests everything...)"
  task :run, [:name_of_application, :verbose] do |_, args|
    args.with_defaults(:name_of_application => "applications")
    args.with_defaults(:verbose => 1)
    puts "Running tests for: #{args.name_of_application}"
    system "DJANGO_ENV=test coverage run --source='.' manage.py test #{args.name_of_application} -v #{args.verbose} --failfast"
  end


  desc "Show test coverage (default: '--show-missing --ignore-errors --skip-covered')"
  task :coverage, [:cli_args] do |_, args|
    args.with_defaults(:cli_args => "--show-missing --ignore-errors --skip-covered")
    system "coverage report #{args.cli_args}"
  end
  
  
  desc "Browse test coverage"
  task :browse_coverage, [:port] do |_, args|
    args.with_defaults(:port => "9001")
    puts "Open your web browser: http://127.0.0.1:#{args.port}"
    system %{
      cd htmlcov/
      python -m http.server #{args.port}
    }
  end
end
