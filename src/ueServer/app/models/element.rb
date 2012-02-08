class Element
  include MongoMapper::Document

  key :elclass, String
  key :eltype, String
  key :elname, String
  key :created_by, String
  timestamps!

  belongs_to :asset
  many :versions
end